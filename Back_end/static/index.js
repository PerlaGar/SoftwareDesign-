document.addEventListener('DOMContentLoaded', function () {
    fetchMovies();
});

function fetchMovies() {
    fetch('http://localhost:5000/movies')
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('movies-container');
        container.innerHTML = ''; // Clear previous content
        data.movies.forEach(movie => {
            const movieElement = document.createElement('div');
            movieElement.classList.add('movie-item');
            movieElement.innerHTML = `
                <img src="${movie.image}" alt="${movie.name}" class="movie-image">
                <h2>${movie.name} (${movie.status}) - $${movie.price}</h2>
                <p><strong>IMDB:</strong> ${movie.imdb}</p>
                <p class="movie-overview">${movie.overview}</p>
            `;
                container.appendChild(movieElement);
            });
        })
        .catch(error => console.error('Error fetching movies:', error));
}