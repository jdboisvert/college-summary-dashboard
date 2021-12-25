function getYearValues(stats) {
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
    const newestProgramsElement = document.getElementById("newestPrograms")

    const yearlyStats = getYearValues(newestProgramsElement.dataset.counts);
    const keys = Object.keys(yearlyStats);

    //Build an array of the values that match the key
    values = []
    for (let i = 0; i < keys.length; i++) {
        values.push(yearlyStats[keys[i]]);
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
    $('#latestPrograms').after('<div id="nav"></div>');
    var rowsShown = 7;
    var rowsTotal = $('#latestPrograms tbody tr').length;
    var numPages = rowsTotal / rowsShown;
    for (i = 0; i < numPages; i++) {
        var pageNum = i + 1;
        $('#nav').append('| <a href="#latestProgram" rel="' + i + '">' + pageNum + '</a> ');
    }
    $('#latestPrograms tbody tr').hide();
    $('#latestPrograms tbody tr').slice(0, rowsShown).show();
    $('#nav a:first').addClass('active');
    $('#nav a').bind('click', function() {

        $('#nav a').removeClass('active');
        $(this).addClass('active');
        var currPage = $(this).attr('rel');
        var startItem = currPage * rowsShown;
        var endItem = startItem + rowsShown;
        $('#latestPrograms tbody tr').css('opacity', '0.0').hide().slice(startItem, endItem).
        css('display', 'table-row').animate({
            opacity: 1
        }, 300);
    });

}

document.addEventListener("DOMContentLoaded", function(event) {
     makeLatestProgramsTablePaginate();
     makeYearlyPieChart();
});
