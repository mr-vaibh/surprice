$(document).ready(function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const btnClass = `bg-gray-700 text-white px-2 py-1 rounded-lg shadow-lg hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 transition duration-200`

    // Load sports data into the table
    function loadSports() {
        $.get("/sports/", function (data) {
            const tableBody = $("#sportsTable");
            tableBody.empty();
            data.forEach(sport => tableBody.append(createSportRow(sport)));
        }).fail(() => alert("Error loading sports."));
    }

    // Format default pricing
    function formatDefaultPricings(pricings) {
        if (!pricings || pricings.length === 0) return "No pricings";
        return pricings.map(pricings => createPricingsTable(pricings)).join('');
    }

    // Create default pricings table
    function createPricingsTable(pricing) {
        const tableHeader = `<table class="min-w-full table-auto"><col style="width:50%"><col style="width:50%"><tbody>`;
        const tableFooter = `</tbody></table>`;

        return tableHeader + createPricingTableRow(pricing) + tableFooter;
    }

    // Create specific pricing rows
    function createPricingTableRow(pricing) {
        return `<tr id="pricing-${pricing.id}">
                    <td>${pricing.duration}</td>
                    <td>$${pricing.price}</td>
                    <td><button class="${btnClass}" onclick="deletePricing(${pricing.id})"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
    }

    // Format pricing overrides
    function formatPriceOverrides(overrides) {
        if (!overrides || overrides.length === 0) return "No overrides";
        return overrides.map(override => createOverrideTable(override)).join('');
    }

    // Create pricing override table
    function createOverrideTable(override) {
        const formattedPrice = formatOverridePrice(override);
        const tableHeader = `<table class="min-w-full table-auto"><col style="width:50%"><col style="width:50%"><tbody>`;
        const tableFooter = `</tbody></table>`;

        if (override.override_type === 'datetime') {
            return tableHeader + createDatetimeOverrideTable(override, formattedPrice) + tableFooter;
        } else if (override.override_type === 'daytime') {
            return tableHeader + createDaytimeOverrideTable(override, formattedPrice) + tableFooter;
        } else if (override.override_type === 'timeonly') {
            return tableHeader + createTimeonlyOverrideTable(override, formattedPrice) + tableFooter;
        }
    }

    // Format price with sign and color
    function formatOverridePrice(override) {
        const price = parseFloat(override.price_modifier);
        const color = price < 0 ? 'red' : 'green';
        const sign = price < 0 ? '-' : '+';
        return `${sign} <span style="color: ${color};">$${Math.abs(price).toFixed(2)}</span>`;
    }

    // Create specific override rows
    function createDatetimeOverrideTable(override, formattedPrice) {
        const formattedDate = new Date(override.date).toLocaleDateString();
        const startTime = new Date(`1970-01-01T${override.start_time}`).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const endTime = new Date(`1970-01-01T${override.end_time}`).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        return `<tr id="override-${override.id}">
                    <td>On <b>${formattedDate}</b>, From <b>${startTime}</b> to <b>${endTime}</b></td>
                    <td>${formattedPrice}</td>
                    <td><button class="${btnClass}" onclick="deleteOverride(${override.id})"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
    }

    function createDaytimeOverrideTable(override, formattedPrice) {
        const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const dayName = daysOfWeek[override.day_of_week];

        return `<tr id="override-${override.id}">
                    <td>On <b>${dayName}</b></td>
                    <td>${formattedPrice}</td>
                    <td><button class="${btnClass}" onclick="deleteOverride(${override.id})"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
    }

    function createTimeonlyOverrideTable(override, formattedPrice) {
        const startTime = new Date(`1970-01-01T${override.start_time}`).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const endTime = new Date(`1970-01-01T${override.end_time}`).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        return `<tr id="override-${override.id}">
                    <td>Everyday From <b>${startTime}</b> to <b>${endTime}</b></td>
                    <td>${formattedPrice}</td>
                    <td><button class="${btnClass}" onclick="deleteOverride(${override.id})"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
    }

    // Create sport row
    function createSportRow(sport) {
        const defaultPricings = formatDefaultPricings(sport.default_pricing);
        const priceOverrides = formatPriceOverrides(sport.pricing_overrides);
        return `<tr id="sport-${sport.id}">
                    <td class="border px-4 py-2">${sport.name}</td>
                    <td class="border px-4 py-2">
                        <button class="${btnClass}" onclick="showAddPricingModal(${sport.id})"><i class="fa-solid fa-plus"></i> </button>
                        <div class="space-y-1">${defaultPricings}</div>
                    </td>
                    <td class="border px-4 py-2">
                        <button class="${btnClass}" onclick="showAddOverrideModal(${sport.id})"><i class="fa-solid fa-plus"></i> </button>
                        <div class="space-y-1">${priceOverrides}</div>
                    </td>
                    <td class="border px-4 py-2">
                        <button class="bg-gray-500 text-white px-2 py-1 rounded" onclick="showUpdateSportModal(${sport.id})">Edit</button>
                        <button class="bg-red-500 text-white px-2 py-1 rounded mt-1" onclick="deleteSport(${sport.id})">Delete</button>
                    </td>
                </tr>`;
    }

    // Delete Default Price
    window.deletePricing = function (priceId) {
        $.ajax({
            url: `/default-pricing/${priceId}/`,
            method: "DELETE",
            headers: { "X-CSRFToken": csrftoken },
            success: function () {
                $(`#pricing-${priceId}`).remove();
                alert("Price deleted successfully!");
            },
            error: function () {
                alert("Error deleting price.");
            }
        });
    };

    // Delete Price Override
    window.deleteOverride = function (overrideId) {
        $.ajax({
            url: `/pricing-overrides/${overrideId}/`,
            method: "DELETE",
            headers: { "X-CSRFToken": csrftoken },
            success: function () {
                $(`#override-${overrideId}`).remove();
                alert("Override deleted successfully!");
            },
            error: function () {
                alert("Error deleting override.");
            }
        });
    };

    // Delete Sport
    window.deleteSport = function (sportId) {
        $.ajax({
            url: `/sports/${sportId}/`,
            method: "DELETE",
            headers: { "X-CSRFToken": csrftoken },
            success: function () {
                $(`#sport-${sportId}`).remove();
                alert("Sport deleted successfully!");
            },
            error: function () {
                alert("Error deleting sport.");
            }
        });
    };

    // Show Update Sport Modal
    window.showUpdateSportModal = function (sportId) {
        $.get(`/sports/${sportId}/`, function (data) {
            $("#sportId").val(data.id);
            $("#updateSportName").val(data.name);
            $("#updateSportDuration").val(data.default_pricing.duration || "");
            $("#updateSportPrice").val(data.default_pricing.price || "");
            $("#updateSportModal").removeClass("hidden");
        }).fail(() => alert("Error fetching sport details."));
    };

    // Handle Update Sport Submission
    $("#updateSportForm").on("submit", function (e) {
        e.preventDefault();

        const sportId = $("#sportId").val();
        const updatedData = {
            name: $("#updateSportName").val(),
        };

        $.ajax({
            url: `/sports/${sportId}/`,
            method: "PUT",
            contentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },
            data: JSON.stringify(updatedData),
            success: function () {
                alert("Sport updated successfully!");
                $("#updateSportModal").addClass("hidden");
                loadSports();
            },
            error: function () {
                alert("Error updating sport.");
            },
        });
    });

    // Show Add Default Pricing Modal
    window.showAddPricingModal = function (sportId) {
        $("#modalPriceSportId").val(sportId);
        $("#defaultPricingModal").removeClass("hidden");
    };

    // Handle Add Default Pricing Form Submission
    $("#defaultPricingForm").on("submit", function (e) {
        e.preventDefault();

        const sportId = $("#modalPriceSportId").val();
        const pricingData = {
            sport: parseInt(sportId),
            duration: $("#durationDefault").val(),
            price: $("#priceDefault").val()
        };

        addPricing(pricingData);
    });

    // Add price override
    function addPricing(pricingData) {
        $.ajax({
            url: "/default-pricing/",
            method: "POST",
            contentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },
            data: JSON.stringify(pricingData),
            success: function () {
                alert("Price added successfully!");
                $("#defaultPricingModal").addClass("hidden");
                loadSports();
            },
            error: function () {
                alert("Error adding pricing.");
            }
        });
    }

    // Show Add Price Override Modal
    window.showAddOverrideModal = function (sportId) {
        $("#modalOverrideSportId").val(sportId);
        $("#priceOverrideModal").removeClass("hidden");
    };

    // Handle Add Price Override Form Submission
    $("#priceOverrideForm").on("submit", function (e) {
        e.preventDefault();

        const sportId = $("#modalOverrideSportId").val();
        const overrideData = {
            sport: parseInt(sportId),
            override_type: $("#overrideType").val(),
            price_modifier: $("#priceModifier").val()
        };

        addOverride(overrideData);
    });

    // Add price override
    function addOverride(overrideData) {
        const overrideType = $("#overrideType").val();

        if (overrideType === "datetime") {
            overrideData.date = $("#datetimeDate").val();
            overrideData.start_time = $("#datetimeStartTime").val();
            overrideData.end_time = $("#datetimeEndTime").val();
        } else if (overrideType === "daytime") {
            overrideData.day_of_week = $("#daytimeDay").val();
        } else if (overrideType === "timeonly") {
            overrideData.start_time = $("#timeonlyStartTime").val();
            overrideData.end_time = $("#timeonlyEndTime").val();
        }

        $.ajax({
            url: "/pricing-overrides/",
            method: "POST",
            contentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },
            data: JSON.stringify(overrideData),
            success: function () {
                alert("Override added successfully!");
                $("#priceOverrideModal").addClass("hidden");
                loadSports();
            },
            error: function () {
                alert("Error adding override.");
            }
        });
    }

    // Show Add Sport Modal
    window.showAddSportModal = function () {
        $("#addSportModal").removeClass("hidden");
    };

    // Add New Sport
    $("#addSportForm").on("submit", function (e) {
        e.preventDefault();

        const newSportData = {
            name: $("#addSportName").val(),
        };

        $.ajax({
            url: "/sports/",
            method: "POST",
            contentType: "application/json",
            headers: { "X-CSRFToken": csrftoken },
            data: JSON.stringify(newSportData),
            success: function () {
                $("#addSportModal").addClass("hidden");
                loadSports();
            },
            error: function () {
                alert("Error occurred while creating Sport.");
            }
        });
    });

    // Close modal
    window.closeModal = function (modalId) {
        $(`#${modalId}`).addClass("hidden");
    };

    // Handle override type selection
    $("#overrideType").change(function () {
        const selectedType = $(this).val();
        $("#datetimeFields, #daytimeFields, #timeonlyFields").addClass("hidden");

        if (selectedType === "datetime") {
            $("#datetimeFields").removeClass("hidden");
        } else if (selectedType === "daytime") {
            $("#daytimeFields").removeClass("hidden");
        } else if (selectedType === "timeonly") {
            $("#timeonlyFields").removeClass("hidden");
        }
    });

    // Initial load of sports
    loadSports();
});
