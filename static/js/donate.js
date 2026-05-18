    const scrollContainer = document.getElementById('scrollableContent');
    const progressBar = document.getElementById('scrollProgressBar');

    scrollContainer.addEventListener('scroll', () => {
        const scrollTop = scrollContainer.scrollTop;
        const scrollHeight = scrollContainer.scrollHeight - scrollContainer.clientHeight;
        
        if (scrollHeight > 0) {
            const scrolledPercentage = (scrollTop / scrollHeight) * 100;
            progressBar.style.width = scrolledPercentage + '%';
        }
    });
