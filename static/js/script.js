document.addEventListener('DOMContentLoaded', function() {
    const splitForm = document.getElementById('splitForm');
    const reconstructForm = document.getElementById('reconstructForm');
    const addShareBtn = document.getElementById('addShareBtn');
    const shareInputs = document.getElementById('shareInputs');
    const splitResult = document.getElementById('splitResult');
    const reconstructResult = document.getElementById('reconstructResult');

    splitForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const seed = document.getElementById('seed').value;
        const shares = document.getElementById('shares').value;
        const threshold = document.getElementById('threshold').value;
        const seedType = document.getElementById('seedType').value;

        fetch('/split', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'seed': seed,
                'shares': shares,
                'threshold': threshold,
                'seedType': seedType
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                splitResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                let sharesHtml = '<h3>Generated Share IDs:</h3><ul>';
                data.share_ids.forEach((shareId, index) => {
                    sharesHtml += `<li>Share ID ${index + 1}: ${shareId}</li>`;
                });
                sharesHtml += '</ul>';
                splitResult.innerHTML = `<div class="alert alert-success">${sharesHtml}</div>`;
            }
        })
        .catch(error => {
            splitResult.innerHTML = `<div class="alert alert-danger">An error occurred: ${error}</div>`;
        });
    });

    reconstructForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const shareIds = Array.from(document.getElementsByClassName('share-input'))
            .map(input => input.value.trim())
            .filter(value => value !== '');
        const seedType = document.getElementById('reconstructSeedType').value;

        if (shareIds.length < 2) {
            reconstructResult.innerHTML = `<div class="alert alert-danger">At least 2 shares are required</div>`;
            return;
        }

        fetch('/reconstruct', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ share_ids: shareIds, seedType: seedType })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                reconstructResult.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                reconstructResult.innerHTML = `<div class="alert alert-success"><h3>Reconstructed Seed:</h3><p>${data.seed}</p></div>`;
            }
        })
        .catch(error => {
            reconstructResult.innerHTML = `<div class="alert alert-danger">An error occurred: ${error}</div>`;
        });
    });

    addShareBtn.addEventListener('click', function() {
        const shareCount = shareInputs.children.length + 1;
        const newShareInput = document.createElement('div');
        newShareInput.className = 'mb-3';
        newShareInput.innerHTML = `
            <label for="share${shareCount}" class="form-label">Share ID ${shareCount}</label>
            <input type="text" class="form-control share-input" id="share${shareCount}">
        `;
        shareInputs.appendChild(newShareInput);
    });
});
