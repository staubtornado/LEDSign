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
const version = document.getElementById('version');

function updateInfo() {
    fetch('/api/info')
        .then(response => response)
        .then(async data => {
            data = await data.json();
            temp.innerHTML = data.temp;
            network.innerHTML = data.network;
            version.innerHTML = data.version;
        })
        .catch(error => {
            console.error(error);
        });
    setTimeout(updateInfo, 5000);
}
updateInfo();