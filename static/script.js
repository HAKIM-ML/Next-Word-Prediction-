document.getElementById('seed_text').addEventListener('input', function() {
    var seedText = this.value;
    if (seedText.trim() === '') {
        document.getElementById('recommendations').innerHTML = '';
        return;
    }

    fetch('/predict', {
        method: 'POST',
        body: new URLSearchParams({
            'seed_text': seedText
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        var recommendationsHTML = '';
        data.recommendations.forEach(function(recommendation, index) {
            // Add bold-text class to the first recommendation
            var className = index === 0 ? 'bold-text' : '';
            recommendationsHTML += '<p class="' + className + '">' + recommendation + '</p>';
        });
        document.getElementById('recommendations').innerHTML = recommendationsHTML;
    });
});
