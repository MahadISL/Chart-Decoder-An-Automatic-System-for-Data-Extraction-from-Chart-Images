$(document).ready(function () {
    // Init
    $('.table').hide();
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#btn-classify').show();
    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });
    $('.classify-section').hide();
    $('.loader').hide();
    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

       

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
               
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
            },
        
        });
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#imagePreview1').css('background-image', 'url(' + e.target.result + ')');
                    $('#imagePreview1').hide();
                    $('#imagePreview1').fadeIn(650);
                }
                reader.readAsDataURL(input.files[0]);
                }
        }
        $("#imageUpload1").change(function () {
        $('.classify-section').show();
        readURL(this);
        });
        
    });
    $('.container-fluid').hide();
    $('#btnID').click(function show () {
        
        $('.container-fluid').show();
        $("#imageUpload").change(function () {
            $('.container-fluid').show();
            readURL(this);
        });
        
        let image = document.getElementById("image");

        image.src = "/static/classify/abc.jpg"
        return image.src
        
    });

    $('#btnID').click(function show () {
        
        $('.container-fluid').show();
        $("#imageUpload").change(function () {
            $('.container-fluid').show();
            readURL(this);
        });
        
        let image = document.getElementById("image1");

        image.src = "/static/classify/abc.jpg"
        return image.src
        
    });

    $('.object_detect').hide();
    $('#btnID2').click(function show () {
        
        $('.object_detect').show();
        $("#classupload").change(function () {
            $('.object_detect').show();
            readURL(this);
        });
        
        let image = document.getElementById("image2");

        image.src = "/static/detection/abc.jpg"
        return image.src
        
    });

    $('#btnID2').click(function show () {
        
        $('.object_detect').show();
        $("#classupload").change(function () {
            $('.object_detect').show();
            readURL(this);
        });
        
        let image = document.getElementById("image2");

        image.src = "/static/detection/image0.jpg"
        return image.src
        
    });

    // Predict
    $('#btn-classify').show();
    $('#btn-classify').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/classify',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result1').fadeIn(600);
                $('#result1').text(' Result:  ' + data);
                console.log('Success!');
            },
        
        });
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#imagePreview1').css('background-image', 'url(' + e.target.result + ')');
                    $('#imagePreview1').hide();
                    $('#imagePreview1').fadeIn(650);
                }
                reader.readAsDataURL(input.files[0]);
                }
        }
        let image = document.getElementById("image5");

        image.src = "/static/classify/abc.jpg"
        
        $("#imageUpload1").change(function () {
        $('.classify-section').show();
        readURL(this);
        });
        return image.src
    });


    $('#btn-detect').show();
    $('#btn-detect').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/detection',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result1').fadeIn(600);
                $('#result1').text(' Result:  ' + data);
                console.log('Success!');
            },
        
        });
        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('#imagePreview1').css('background-image', 'url(' + e.target.result + ')');
                    $('#imagePreview1').hide();
                    $('#imagePreview1').fadeIn(650);
                }
                reader.readAsDataURL(input.files[0]);
                }
        }
        let image = document.getElementById("image6");

        image.src = "/static/detection/image0.jpg"


        $("#imageUpload1").change(function () {
        $('.classify-section').show();
        readURL(this);
        });
        return image.src
    });
    $("#center").change(function () {

        $('#center').show();
        readURL(this);
    });
    $('#refreshtb').click(function () {

        location.reload(true);
        console.log('success')
    });
    $('#refreshtb').click(function show () {

        $('.center').show();
        $("#center").change(function () {
            $('.center').show();
            readURL(this);
        });

        location.reload(true);
        console.log('success')

    });
});