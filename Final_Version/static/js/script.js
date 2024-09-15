// FUNCTIONS for Voicemed

// September 2024

// Avoid screen reload
document.getElementById('manual_input_form').addEventListener('submit', async function(event) {
    event.preventDefault(); } // Prevent page reload
);

document.getElementById('text_input_section').addEventListener('submit', async function(event) {
    event.preventDefault(); } // Prevent page reload
);

function start_scan() {
    document.getElementById("medication_code_input").style.display = "none";
    //document.getElementById("main_gradient").style.display = "none";
    document.getElementById("medication_scanner").style.display = "flex";
    document.body.style.overflow = 'hidden';
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

        global_drug_code = input;

        // Show loading screen (simple spinner loader, it's a fast request)
        document.getElementById("medication_code_input").style.display = "none";
        document.getElementById("spinner_loader").style.display = "flex";
        document.body.style.overflow = 'hidden';

        // Make the basic information request
        fetch('/manualcode', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: input }) // Send the code in the request body
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Parse the JSON response
            } else {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
        })
        .then(data => {
            // Set the medication information
            clearInterval(cam_interval);
            clearInterval(result_interval);
            show_medication_information(capitalizeFirstLetterOfEachWord(data.name), data.manufacturer_name);
        })
        .catch(error => {
            console.error('Error:', error);
        });

    }

    else {
        show_manual_code_error();
    }

}



// Medication information
function show_medication_information(name, merchant) {

    // Add to the conversation
    add_conversation(name);
    
    document.getElementById("medication_big_name").innerHTML = "💊 &nbsp; " + name;
    document.getElementById("medication_big_detail").innerHTML = merchant;

    document.getElementById("main_gradient").style.display = "none";
    document.getElementById("spinner_loader").style.display = "none";
    document.getElementById("medication_voice_question").style.display = "block";

}




// SPEECH RECOGNITION

function start_speech_recognition() {

    // Check if the browser supports speech recognition
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false; // Keep recognizing even if the user pauses
        recognition.interimResults = true; // Show interim results before finalizing
        recognition.lang = 'en-US';

        // Event handler for when speech is recognized
        recognition.onresult = function(event) {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            document.getElementById("final_voice_transcription").innerHTML = transcript;
        };

        // Event handler for errors
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
        };

        recognition.onstart = function() {
            document.getElementById("mic_off").style.display = 'none';
            document.getElementById("mic_on").style.display = 'block';
            document.getElementById("mic_button").style.backgroundColor = '#7fb3d5';
        };

        recognition.onend = function() {
            document.getElementById("mic_off").style.display = 'block';
            document.getElementById("mic_on").style.display = 'none';
            document.getElementById("mic_button").style.backgroundColor = 'rgb(26 86 219/var(--tw-bg-opacity))';
            document.getElementById("final_voice_transcription").style.color = 'black';

            answer_question(document.getElementById("final_voice_transcription").innerHTML);
        
        };

        recognition.onstart

        // Start recognition
        recognition.start();
    } else {
        console.error('Speech recognition not supported in this browser.');
    }


}




// Ask question from text
function ask_question_from_text() {

    var text = document.getElementById("comment_area").value;
    answer_question(text);

}


// Switch to speech recognition
function switch_voice_recognition() {

    document.getElementById("text_input_section").style.display = "none";
    document.getElementById("suggested_questions").style.display = "none";
    document.getElementById("mic_section").style.display = "flex";

}


function switch_text_input() {

    document.getElementById("mic_section").style.display = "none";
    document.getElementById("text_input_section").style.display = "block";
}


function switch_to_examples() {
    document.getElementById("text_input_section").style.display = "none";
    document.getElementById("suggested_questions").style.display = "block";
}



// Bottom bar
function clear_conversations() {
    
    // Clear the conversation bar
    const elements = document.querySelectorAll('.user_added');

    // Iterate over each element and remove its class attributes
    elements.forEach(element => {
    element.className = '';
    });
}


function add_conversation(conversation_name) {

    // Add a new conversation to the conversation bar
    var template = `
    <li class="user_added">
        <a href="#" class="flex items-center p-2 text-base font-medium text-gray-900 rounded-lg transition duration-75 hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-white group"
        >
        <svg class="w-6 h-6 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
            <path fill-rule="evenodd" d="M3.559 4.544c.355-.35.834-.544 1.33-.544H19.11c.496 0 .975.194 1.33.544.356.35.559.829.559 1.331v9.25c0 .502-.203.981-.559 1.331-.355.35-.834.544-1.33.544H15.5l-2.7 3.6a1 1 0 0 1-1.6 0L8.5 17H4.889c-.496 0-.975-.194-1.33-.544A1.868 1.868 0 0 1 3 15.125v-9.25c0-.502.203-.981.559-1.331ZM7.556 7.5a1 1 0 1 0 0 2h8a1 1 0 0 0 0-2h-8Zm0 3.5a1 1 0 1 0 0 2H12a1 1 0 1 0 0-2H7.556Z" clip-rule="evenodd"/>
        </svg>
        
        <span class="ml-3">${conversation_name}</span>
        </a>
    </li>
    `;

    // Create a temporary container to hold the HTML string
    var temp_container = document.createElement('div');

    // Set the innerHTML of the container to the template
    temp_container.innerHTML = template;

    document.getElementById("vertical_bar_menu").appendChild(temp_container.firstElementChild);

}




// Question-answering functions
function answer_question(text) {

    // Hide placehodler and show loader
    document.getElementById("placeholder_section").style.display = 'none';
    document.getElementById("content_section").style.display = 'none';
    document.getElementById("yes_no_response_icon").style.display = 'none';
    document.getElementById("skeleton_section").style.display = 'flex';

    // Call groq text and global_data
    // Make an API request to Flask backend
    fetch('/ask_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: text, code: global_drug_code}),
    })
    .then(response => response.text())
    .then(data => {
        console.log("Response from server:", data);
        process_answer(data);
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById("skeleton_section").style.display = 'none';
        document.getElementById("content_section").innerText = 'Error retrieving answer.';
    });

}


function process_answer(answer) {

    // Set icon images if detected
    if (answer.toLowerCase().includes("yes")) {
        document.getElementById("yes_no_response_icon").style.display = 'block';
        document.getElementById("yes_no_response_icon").src = "/static/images/yes.png";
    }

    else if (answer.toLowerCase().includes("no")) {
        document.getElementById("yes_no_response_icon").style.display = 'block';
        document.getElementById("yes_no_response_icon").src = "/static/images/no.png";
    }

    // Set the answer text
    document.getElementById("llm_answer").innerHTML = answer;

    // Hide loader and show content
    document.getElementById("skeleton_section").style.display = 'none';
    document.getElementById("content_section").style.display = 'block';


}