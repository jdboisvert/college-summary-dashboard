function getYearValues(stats) {
    console.log(stats)
    const yearCountsStr = stats['Year Counts'];
    const yearCountsUnFormatted = yearCountsStr.split(',');
    const yearCounts = {};

    for (let i = 0; i < yearCountsUnFormatted.length; i++) {

        const values = yearCountsUnFormatted[i].split(':');
        yearCounts[values[0].replace(/[^0-9]/g, '')] = values[1].replace(/[^0-9]/g, '');

    }

    return yearCounts;
}

function makeYearlyPieChart() {
    const newestProgramsElement = document.getElementById("newest-programs")

    const yearlyStats = JSON.parse(newestProgramsElement.dataset.counts.replace(/'/g, '"'));

    //Build an array of the values that match the key
    const values = [];
    const keys = [];
    for (const year in yearlyStats) {
        keys.push(year);
        values.push(yearlyStats[year]);
    }

    var ctx = newestProgramsElement.getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: keys,
            datasets: [{
                data: values,
                //Extra colors are added in case there are more than 6 years present
                backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255,140,0)", "rgb(34,139,34)", "rgb(128,0,128)", "rgb(255, 180, 86)", "rgb(165,42,42)", "rgb(128,128,128)"]
            }]

        },
    });

}

function makeLatestProgramsTablePaginate() {
    // TODO remove jQuery logic here.
    $('#latest-programs').after('<div id="nav"></div>');
    var rowsShown = 7;
    var rowsTotal = $('#latest-programs tbody tr').length;
    var numPages = rowsTotal / rowsShown;
    for (i = 0; i < numPages; i++) {
        var pageNum = i + 1;
        const link = `${pageNum != 1 ? "| " : ""} <a href="#latest-program-anchor" rel="${i}">${pageNum} </a>`

        $('#nav').append(link);
    }
    $('#latest-programs tbody tr').hide();
    $('#latest-programs tbody tr').slice(0, rowsShown).show();
    $('#nav a:first').addClass('active');
    $('#nav a').bind('click', function() {

        $('#nav a').removeClass('active');
        $(this).addClass('active');
        var currPage = $(this).attr('rel');
        var startItem = currPage * rowsShown;
        var endItem = startItem + rowsShown;
        $('#latest-programs tbody tr').css('opacity', '0.0').hide().slice(startItem, endItem).
        css('display', 'table-row').animate({
            opacity: 1
        }, 300);
    });

}

document.addEventListener("DOMContentLoaded", function(event) {
     makeLatestProgramsTablePaginate();
     makeYearlyPieChart();
});
