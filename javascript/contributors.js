async function fetchContributors() {
    const response = await fetch('https://api.github.com/repos/dxmxtrxs/netscan/contributors');
    const contributors = await response.json();
    const totalContributions = contributors.reduce((sum, contributor) => sum + contributor.contributions, 0);

    const contributorsList = document.getElementById('contributors-list');
    contributorsList.innerHTML = '';

    contributors.forEach(contributor => {
        const contributionPercentage = ((contributor.contributions / totalContributions) * 100).toFixed(2);

        const contributorItem = document.createElement('li');
        contributorItem.className = 'contributor';

        contributorItem.innerHTML = `
            <a href="${contributor.html_url}" target="_blank">
                <img src="${contributor.avatar_url}" alt="${contributor.login}">
                <p>${contributor.login}</p>
                <p>${contributionPercentage}%</p>
            </a>
        `;

        contributorsList.appendChild(contributorItem);
    });
}

fetchContributors();
