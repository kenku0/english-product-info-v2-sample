async function generate(inputId) {
    const inputBox = document.getElementById(`input${inputId}`);
    const outputBox = document.getElementById(`output${inputId}`);
    const generateButton = document.getElementById(`generate${inputId}`);
    const copyButton = document.getElementById(`copy${inputId}`);
    let tableHTML = ""; // Initialize here

    
// Show loading state
    if (generateButton) {
        generateButton.textContent = "Generating...";
        generateButton.disabled = true;
    }

    try {
        let response = await fetch(`/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'idx': String(inputId),
                'text': inputBox.value
            })
        });

        let data;
        if (response.ok) {
            let responseText = await response.text();
            data = JSON.parse(responseText); // Add this line to parse the response text into JSON
            copyButton.style.display = 'block';
            inputBox.value = ''; // Clear input after generation

            if (data.error) {
                alert('Error: ' + data.error);
                generateButton.textContent = "Generate"; // Reset the button text even on error
                generateButton.disabled = false;
                return;
                }   
        } else {
            alert('Error: ' + response.statusText);
        }   
    
        let output = data.output;
        
        if (outputBox.innerHTML.trim() !== '') {
            outputBox.innerHTML += '<br>'; // Separate tables with a line break
            }

            let tableHTML = '<table class="table"><thead>';
    
            // Only create table headers if the output box is empty
            if(inputId == 2) {
                tableHTML += '<table class="table"><thead><tr><th>Inputted Title</th><th>Finalized Description (Review-Ready)</th><th>Concerns with Description</th><th>Property</th><th>Quality of Finalized Description</th></tr></thead><tbody>';
            } else {
                tableHTML += '<table class="table"><thead><tr><th>Inputted Title</th><th>Inputted Title: Score<th>Translated Title</th><th>Refined Title (SEO-Optimized)</th><th>Refined Title: Concerns</th><th>Finalized Title (Mainstream-Friendly)</th><th>Finalized Title: Score</th></tr></thead><tbody>';
            }

        for (let i = 2; i < output.length; i++) {
            let quality = output[i][output[i].length - 1]; // Get quality score from last column

            if (quality <= 8) {
                rowHTML = "<tr class='quality8'>"; // Highlight dark yellow

            } else {
                rowHTML = "<tr>";
            }

            let numColumns = output[i].length;
            
            for (let j = 0; j < numColumns; j++) {
                rowHTML += `<td>${output[i][j]}</td>`;
            }
            
            rowHTML += "</tr>";
            tableHTML += rowHTML;
        }

         tableHTML += '</tbody></table>';
 
         outputBox.innerHTML = tableHTML;
        outputBox.classList.remove('invisible');

    } catch (error) {
        console.error('An error occurred:', error);
        generateButton.textContent = "Generate";
        generateButton.disabled = false;
        alert('Error: ' + response.statusText);
    }  
    
    // Revert button state
    generateButton.textContent = "Generate";
    generateButton.disabled = false;

}


    
// copy the contents of the output box to the clipboard
function copyToClipboard(outputId) {
    let outputBox = document.getElementById(`output${outputId}`);
    if (!outputBox) {
        console.error(`outputBox with id output${outputId} is not found`);
        return;
    }
    let tableRows = outputBox.querySelectorAll('.table tbody tr');
    let copiedText = "Segment, Original Title, Initial Title (Translated), SEO-Optimized Title (Refined), Concerns with SEO-Optimized Title, Finalized Title (Review-Ready), Quality of Finalized Title\n";

    for (let i = 0; i < tableRows.length; i++) {
        let rowCells = tableRows[i].querySelectorAll('td');
        let rowText = "";
        for (let j = 0; j < rowCells.length; j++) {
            rowText += rowCells[j].textContent + ", ";
        }
        copiedText += rowText + "\n";
    }

    if (tableRows.length === 0) {
        console.error(`No rows found in outputBox with id output${outputId}`);
        return;
    }

    navigator.clipboard.writeText(copiedText).then(function() {
        let copyToast = document.createElement("div");
        copyToast.innerText = "Content copied to clipboard";
        copyToast.style.position = "fixed";
        copyToast.style.bottom = "20px";
        copyToast.style.right = "20px";
        copyToast.style.padding = "10px";
        copyToast.style.color = "white";
        copyToast.style.backgroundColor = "#333";
        copyToast.style.borderRadius = "5px";
        document.body.appendChild(copyToast);
        setTimeout(function () {
            document.body.removeChild(copyToast);
        }, 2000);
    }, function(err) {
        alert('Failed to copy text');
    });
}

 // Add event listeners for 'Enter' keypress on input boxes
for (let i = 1; i <= 2; i++) {
    let inputElement = document.getElementById(`input${i}`);

    if (inputElement) {
        inputElement.addEventListener('keydown', function(event) {
            console.log(`Key pressed: ${event.key}`);
            console.log(`Shift key status: ${event.shiftKey}`);

            if (event.key === 'Enter' && !event.shiftKey) {
                console.log('Enter key pressed without Shift');
                event.preventDefault();

                if (typeof generate === "function") {
                    console.log('Calling generate function');
                    generate(i);
                } else {
                    console.error('generate is not a defined function');
                }
            }
        });
    } else {
        console.error(`Element with id input${i} is not found`);
    }
}

// When the document has finished loading, adjust the width of all elements to fit the table
window.addEventListener('load', function() {
    let table = document.querySelector('.table');
    if(table) {
        let width = `${table.offsetWidth}px`;
        document.body.style.width = width;
        
        let allContainerElements = document.querySelectorAll('.container');
        allContainerElements.forEach(element => {
            element.style.width = width;
        });
    } else {
        document.body.style.width = '100%';
    }

    let generateButton = document.querySelector("#generate");
    let copyButton = document.querySelector("#copy");
    
    if (generateButton) generateButton.style.order = "1";
    if (copyButton) copyButton.style.order = "2";
});