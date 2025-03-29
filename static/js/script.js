$(document).ready(function () {
    let file;  // Store selected file

    // Dark Mode Toggle
    $("#dark-mode-toggle").click(function () {
        $("body").toggleClass("dark-mode light-mode");

        // Change button icon and text
        let isDark = $("body").hasClass("dark-mode");
        $(this).html(isDark ? '<i class="fas fa-sun"></i> Light Mode' : '<i class="fas fa-moon"></i> Dark Mode');
    });

    // Handle Drag & Drop
    $("#drop-area").on("dragover", function (e) {
        e.preventDefault();
        $(this).css("background-color", "#e3f2fd");
    });

    $("#drop-area").on("dragleave", function () {
        $(this).css("background-color", "#ffffff");
    });

    $("#drop-area").on("drop", function (e) {
        e.preventDefault();
        file = e.originalEvent.dataTransfer.files[0];
        showPreview(file);
    });

    // Handle File Browse Click
    $(".browse-btn").click(function () {
        $("#file-input").click();
    });

    $("#file-input").change(function (event) {
        file = event.target.files[0];
        showPreview(file);
    });

    // Show Image Preview
    function showPreview(file) {
        if (file) {
            let reader = new FileReader();
            reader.onload = function (e) {
                $("#preview-image").attr("src", e.target.result).removeClass("d-none").addClass("d-block");
                $("#upload-btn").removeClass("d-none").addClass("d-block");
            };
            reader.readAsDataURL(file);
        }
    }

    // Handle Image Upload
    $("#upload-btn").click(function () {
        let formData = new FormData();
        formData.append("file", file);

        $("#upload-btn").text("Processing...").prop("disabled", true);
        $("#loading-spinner").removeClass("d-none").addClass("d-block");

        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                $("#loading-spinner").addClass("d-none");
                $("#result-image").attr("src", response.output);
                $("#result-container").removeClass("d-none").addClass("d-block");
                $("#upload-btn").text("Upload & Detect").prop("disabled", false);
            },
            error: function () {
                alert("Error processing image!");
                $("#upload-btn").text("Upload & Detect").prop("disabled", false);
                $("#loading-spinner").addClass("d-none");
            }
        });
    });
});
