async function generatePrompt(){

    const prompt =
        document.getElementById("prompt").value;

    const style =
        document.getElementById("style").value;

    if(prompt.trim()===""){

        alert("Please enter a prompt");

        return;
    }

    document.getElementById("output").innerHTML =
    `
    <div class="card">
        Generating prompt...
    </div>
    `;

    const response = await fetch("/generate", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            prompt:prompt,
            style:style
        })

    });

    const data = await response.json();

    if(data.success){

        document.getElementById("output").innerHTML =

        `
        <div class="card">

            <h2>${style}</h2>

            <div
                id="generatedPrompt"
                class="prompt-box">

                ${data.result}

            </div>

            <button
                class="copy-btn"
                onclick="copyPrompt()">

                Copy Prompt

            </button>

        </div>
        `;
    }
    else{

        document.getElementById("output").innerHTML =

        `
        <div class="card">
            Error: ${data.error}
        </div>
        `;
    }
}


function copyPrompt(){

    const text =
        document.getElementById(
            "generatedPrompt"
        ).innerText;

    navigator.clipboard.writeText(text);

    alert("Prompt copied!");
}