var FOLDER_ALL_CASES = false;
var ERROR_INFOS = [];
var current_error_idx = -1;

function clamp(value, min, max) {
    return Math.max(min, Math.min(value, max));
}

function setFolderBodyVisible(folderBody, visible) {
    folderBody.style.display = visible ? "block" : "none";

    var header = folderBody.previousElementSibling;
    if (header && header.classList.contains("folder_header")) {
        header.classList.toggle("is-collapsed", !visible);
        header.setAttribute("aria-expanded", visible ? "true" : "false");
    }
}

function updateDisplayModeButton() {
    var button = document.getElementById("display_mode");
    if (!button) {
        return;
    }

    var summaryLabel = button.dataset.summaryLabel || "Summary";
    var detailLabel = button.dataset.detailLabel || "Detail";
    var summaryTitle = button.dataset.summaryTitle || "Switch to detail mode";
    var detailTitle = button.dataset.detailTitle || "Switch to summary mode";

    button.textContent = FOLDER_ALL_CASES ? summaryLabel : detailLabel;
    button.title = FOLDER_ALL_CASES ? summaryTitle : detailTitle;

    document.body.classList.toggle("summary-mode", FOLDER_ALL_CASES);
}

function updateErrorCounter() {
    var counter = document.getElementById("error_counter");
    var navButtons = document.querySelectorAll(".error-nav");

    if (!counter) {
        return;
    }

    var emptyLabel = counter.dataset.emptyLabel || "No Errors";
    var prefixLabel = counter.dataset.prefixLabel || "Errors";

    if (!ERROR_INFOS.length) {
        counter.textContent = emptyLabel;
        navButtons.forEach(function(button) {
            button.classList.add("menu-item-disabled");
        });
        return;
    }

    var currentDisplay = current_error_idx >= 0 ? current_error_idx + 1 : 0;
    counter.textContent = prefixLabel + " " + currentDisplay + "/" + ERROR_INFOS.length;
    navButtons.forEach(function(button) {
        button.classList.remove("menu-item-disabled");
    });
}

function focusError(index) {
    if (!ERROR_INFOS.length) {
        return;
    }

    current_error_idx = clamp(index, 0, ERROR_INFOS.length - 1);

    ERROR_INFOS.forEach(function(errorElement) {
        errorElement.classList.remove("error-focus");
    });

    var error = ERROR_INFOS[current_error_idx];
    error.classList.add("error-focus");
    error.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });
    updateErrorCounter();
}

window.addEventListener("load", function() {
    document.querySelectorAll(".folder_header").forEach(function(header) {
        var folderBody = header.nextElementSibling;
        if (!folderBody || !folderBody.classList.contains("folder_body")) {
            return;
        }

        header.setAttribute("aria-expanded", "true");
        header.addEventListener("click", function(event) {
            var currentHeader = event.target.closest(".folder_header");
            var currentBody = currentHeader.nextElementSibling;
            setFolderBodyVisible(currentBody, currentBody.style.display === "none");
        });
    });

    ERROR_INFOS = Array.from(document.querySelectorAll(".error-info, .abort-info"));
    ERROR_INFOS.forEach(function(errorElement, index) {
        errorElement.addEventListener("click", function() {
            focusError(index);
        });
    });

    var errorJumper = document.querySelector(".error_jumper");
    if (errorJumper) {
        errorJumper.style.display = ERROR_INFOS.length ? "flex" : "none";
    }

    updateDisplayModeButton();
    updateErrorCounter();
});

function toggle_folder_all_cases() {
    FOLDER_ALL_CASES = !FOLDER_ALL_CASES;

    document.querySelectorAll(".folder_body").forEach(function(folderBody) {
        setFolderBodyVisible(folderBody, !FOLDER_ALL_CASES);
    });

    updateDisplayModeButton();
}

function previous_error() {
    if (!ERROR_INFOS.length) {
        return;
    }

    if (FOLDER_ALL_CASES) {
        toggle_folder_all_cases();
    }

    var nextIndex = current_error_idx <= 0 ? 0 : current_error_idx - 1;
    focusError(nextIndex);
}

function next_error() {
    if (!ERROR_INFOS.length) {
        return;
    }

    if (FOLDER_ALL_CASES) {
        toggle_folder_all_cases();
    }

    var nextIndex = current_error_idx < 0 ? 0 : current_error_idx + 1;
    focusError(nextIndex);
}
