// FUNCTIONS for Voicemed

// September 2024

function start_scan() {
    alert("WIP");
}


function manual_input() {
    // Display the input form
    document.getElementById("selection_buttons").style.display = "none";
    document.getElementById("manual_input_form").style.display = "block";
}

function selection_method_back() {
    // Display the input form
    document.getElementById("manual_input_form").style.display = "none";
    document.getElementById("selection_buttons").style.display = "block";
}



function show_manual_code_error() {

    var classes = "bg-red-50 border border-red-500 text-red-900 placeholder-red-700 focus:ring-red-500 dark:bg-gray-700 focus:border-red-500 block w-full p-2.5 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500 w-full p-4 ps-10 text-sm text-gray-900 border rounded-lg";
    document.getElementById("manual_pdc_input").className = classes;
    document.getElementById("manual_pdc_errortext").style.display = "block";

}



function validate_pdc_input() {

    var input = document.getElementById("manual_pdc_input").value;

    // Regular expression to match PDC format with hyphens
    const pdcFormatRegex = /^\d{3}-\d{3}-\d{4}$/;

    if (pdcFormatRegex.test(input)) {

        // Allow to continue
        alert("Success!");

    }

    else {
        show_manual_code_error();
    }

}





// SPEECH RECOGNITION

function start_speech_recognition() {

    // Check if the browser supports speech recognition
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false; // Keep recognizing even if the user pauses
        recognition.interimResults = true; // Show interim results before finalizing

        // Event handler for when speech is recognized
        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            document.getElementById("transcription_result").innerHTML = transcript;
        };

        // Event handler for errors
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
        };

        // Start recognition
        recognition.start();
    } else {
        console.error('Speech recognition not supported in this browser.');
    }


}