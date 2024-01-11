const _static = document.getElementById('static');
const s_blink = document.getElementById('s-blink');
const colorInput = document.getElementById('color-input');

function checkRadio() {
    if (_static.checked || s_blink.checked) {
        colorInput.style.display = 'block';
    } else {
        colorInput.style.display = 'none';
    }
}

checkRadio();

const radios = document.getElementsByName('mode');
for (let i = 0; i < radios.length; i++) {
    radios[i].addEventListener('change', checkRadio);
}

document.getElementById('form').addEventListener('change', function () {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    const color = document.getElementById('color-input').value;

    fetch('/api/leds', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({mode, color})
    })
        .then(response => response)
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

const temp = document.getElementById('temp');
const network = document.getElementById('network');

function updateTemp() {
    fetch('/api/temperature')
        .then(response => response)
        .then(async data => {
            temp.innerHTML = await data.text();
        })
        .catch(error => {
            console.error(error);
        });
    setTimeout(updateTemp, 5000);
}

function updateNetwork() {
    fetch('/api/network')
        .then(response => response)
        .then(async data => {
            network.innerHTML = await data.text();
        })
        .catch(error => {
            console.error(error);
        });
    setTimeout(updateNetwork, 10000);
}

updateTemp();
updateNetwork();

fetch('/api/version').then(async response => {
    document.getElementById('version').innerHTML = await response.text();
}).catch(error => {
    console.error(error);
});