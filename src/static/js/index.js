$(window).on("load", () => {
    $("#filter-div").click(() => {
        $("#filter-div").dropdown("show")
    });
    let coterie_filter = {
        name: "",
        type: [],
        address: [],
        day: "",
        age: -1,
        price: -1
    }

    function filter_coteries() {
        $(".coterie").parent().show();
        $(".coterie").parent().filter((i, e) => {
            if (coterie_filter.name !== "") {
                if (!$(e).find(".coterie-name").text().toLowerCase().includes(coterie_filter.name.toLowerCase())) return true;
            }
            if (coterie_filter.type.length !== 0) {
                if (!coterie_filter.type.includes($(e).find(".coterie-type-name").text())) return true;
            }
            if (coterie_filter.address.length !== 0) {
                if (!coterie_filter.address.includes($(e).find(".coterie-address").text())) return true;
            }
            if (coterie_filter.price !== -1) {
                if ($(e).find(".coterie-price").data("p") !== coterie_filter.price) return true;
            }
            if (coterie_filter.age !== -1) {
                let age = $(e).find(".coterie-age").text().split("-");``
                if (coterie_filter.age < Number(age[0]) || Number(age[1].split("\n")[0]) < coterie_filter.age) return true;
            }
            return false;
        }).hide();
    }

    $("#search-query").on("keyup", (e) => {
        coterie_filter.name = $("#search-query").val();
        filter_coteries();
    })
    $("#search-form").submit((e) => {
        e.preventDefault();
        filter_coteries();
    })
    let filter_type_function = (e) => {
        coterie_filter.type = [];
        $(".filter-type").each((i, e) => {
            let selected_type = $(e).val();
            if (selected_type !== "") {
                coterie_filter.type.push(selected_type);
            }
        });
        $("#add-filter-type").show();
        filter_coteries();
    }
    $(".filter-type").change(filter_type_function);
    let close_function_type = (e) => {
        if ($(".filter-type").length === 1) {
            $(".filter-type").prop("selectedIndex", 0);
        } else {
            $(e.target).parent().remove();
        }
        filter_type_function(e);
        filter_coteries();
    }
    $(".close-filter-type").click(close_function_type);
    $("#add-filter-type").click((e) => {
        let clone = $("#filter-type").parent().clone();
        clone.change(filter_type_function)
        clone.find(".close-filter-type").click(close_function_type);
        $("#add-filter-type").before(clone);
    })
    filter_address_function = (e) => {
        coterie_filter.address = [];
        $(".filter-address").each((i, e) => {
            let selected_address = $(e).val();
            if (selected_address !== "") {
                coterie_filter.address.push(selected_address);
            }
        });
        $("#add-filter-address").show();
        filter_coteries();
    }
    $(".filter-address").change(filter_address_function);
    let close_function_address = (e) => {
        if ($(".filter-address").length === 1) {
            $(".filter-address").prop("selectedIndex", 0);
        } else {
            $(e.target).parent().remove();
        }
        filter_address_function(e);
        filter_coteries();
    }
    $(".close-filter-address").click(close_function_address);
    $("#add-filter-address").click((e) => {
        let clone = $("#filter-address").parent().clone();
        clone.change(filter_address_function)
        clone.find(".close-filter-address").click(close_function_address);
        $("#add-filter-address").before(clone);
    })
    $("#filter-price-div > div").click((e) => {
        if ($(e.target).hasClass("active")) {
            $("#filter-price-div > div").removeClass("active")
            coterie_filter.price = -1;
            filter_coteries();
            return
        }
        $("#filter-price-div > div").removeClass("active")
        $(e.target).addClass("active")
        coterie_filter.price = $(e.target).data("price");
        filter_coteries();
    });
    $("#filter-age").change((e) => {
        coterie_filter.age = Number($(e.target).val());
        filter_coteries();
    });
    $(".info").click((e) => {
        $(".modal").modal("hide");
        $(e.target).parent().find(".modal").modal("show");
    })
    $(".close-dropdown").click((e) => {
        e.preventDefault();
        $('.dropdown').dropdown('hide');
    });
    $('body').on('click', function (e) {
        if (($(".dropdown.show").length !== 0
            && !$('.dropdown.show').is(e.target)
            && ($('.dropdown.show').has(e.target).length === 0 || $(".close-dropdown").is(e.target))
            && !$(e.target).is("i.close-filter"))
        ) {
            $('.dropdown').dropdown('hide');
        }
    });
})