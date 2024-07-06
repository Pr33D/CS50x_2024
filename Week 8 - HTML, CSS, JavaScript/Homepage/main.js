document.addEventListener('DOMContentLoaded', () => {

    // What happens, when searchform is submitted on any page
    let bg = document.querySelector('body');
    let searchForm = document.querySelector('#searchForm');

    // listen to submition of search form on every .html page
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();

        let searchText = document.querySelector('#searchText');

        // let something happen by typing special texts
        if (searchText.value == "dark")
            {
                bg.style.backgroundColor = '#9f9f9f';
            }
        else if (searchText.value == "light")
            {
                bg.style.backgroundColor = '';
            }
        else
            {
                alert('please use exclusively light or dark');
            }

        // clear input field char by char
        searchText.value.split('').forEach((c, i) => {
            // async function with time * index of char
            setTimeout(function() {
                let reduced = searchText.value.replace(c, '');
                searchText.value = reduced;
            }, 100 * (i + 1));
        });
    });
});
