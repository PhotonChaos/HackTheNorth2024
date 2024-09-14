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