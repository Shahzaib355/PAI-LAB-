document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const searchBtn = document.getElementById('searchBtn');
    const categorySelect = document.getElementById('category');
    const searchInput = document.getElementById('searchInput');
    const hadithDisplay = document.getElementById('hadithDisplay');
    const searchResults = document.getElementById('searchResults');

    generateBtn.addEventListener('click', generateHadith);
    searchBtn.addEventListener('click', searchHadith);
    
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchHadith();
        }
    });

    function generateHadith() {
        const category = categorySelect.value;
        
        fetch('/get_hadith', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ category: category })
        })
        .then(response => response.json())
        .then(data => {
            displayHadith(data);
            searchResults.classList.remove('active');
        })
        .catch(error => {
            console.error('Error:', error);
            hadithDisplay.innerHTML = '<p class="error">Error loading hadith. Please try again.</p>';
        });
    }

    function displayHadith(hadith) {
        hadithDisplay.innerHTML = `
            <div class="hadith-card">
                <p class="hadith-text">"${hadith.text}"</p>
                <div class="hadith-details">
                    <div class="detail-item">
                        <strong>Reference:</strong> ${hadith.reference}
                    </div>
                    <div class="detail-item">
                        <strong>Book:</strong> ${hadith.book}
                    </div>
                    <div class="detail-item">
                        <strong>Chapter:</strong> ${hadith.chapter}
                    </div>
                    <div class="detail-item">
                        <strong>Narrator:</strong> ${hadith.narrator}
                    </div>
                    <div class="detail-item">
                        <span class="category-badge">${hadith.category}</span>
                    </div>
                </div>
            </div>
        `;
    }

    function searchHadith() {
        const keyword = searchInput.value.trim();
        
        if (keyword === '') {
            alert('Please enter a search keyword');
            return;
        }

        fetch('/search_hadith', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ keyword: keyword })
        })
        .then(response => response.json())
        .then(data => {
            if (data.found) {
                displaySearchResults(data.hadiths);
            } else {
                searchResults.innerHTML = '<div class="no-results">No hadiths found matching your search.</div>';
                searchResults.classList.add('active');
            }
            hadithDisplay.innerHTML = '<div class="welcome-message"><p>Search results displayed below</p></div>';
        })
        .catch(error => {
            console.error('Error:', error);
            searchResults.innerHTML = '<div class="no-results">Error performing search. Please try again.</div>';
            searchResults.classList.add('active');
        });
    }

    function displaySearchResults(hadiths) {
        let resultsHTML = '<h2 style="margin-bottom: 20px; color: #2c3e50;">Search Results (' + hadiths.length + ' found)</h2>';
        
        hadiths.forEach(hadith => {
            resultsHTML += `
                <div class="result-item">
                    <p class="hadith-text">"${hadith.text}"</p>
                    <div class="hadith-details">
                        <div class="detail-item">
                            <strong>Reference:</strong> ${hadith.reference}
                        </div>
                        <div class="detail-item">
                            <strong>Book:</strong> ${hadith.book}
                        </div>
                        <div class="detail-item">
                            <strong>Chapter:</strong> ${hadith.chapter}
                        </div>
                        <div class="detail-item">
                            <strong>Narrator:</strong> ${hadith.narrator}
                        </div>
                        <div class="detail-item">
                            <span class="category-badge">${hadith.category}</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        searchResults.innerHTML = resultsHTML;
        searchResults.classList.add('active');
    }
});
