
/* to use this code, include it and set:

 * lightcurve: a list with source info dicts
 * title: the title of the plot
 * subtitle: the subtitle of the plot

 */

// group per band
var lightcurve_per_band = {};
var error_per_band = {};
var plot_bands_per_series = {};
var plot_bands = [];
var symbols = {0: 'square', 1: 'triangle-down', 2: 'diamond'};

lightcurve.forEach(function(entry) {
    var band = entry["band"];
    var data = {
        x: entry['taustart_ts'],
        y: entry['f_int'],
        f_int: entry['f_int'],
        extract_type: entry['extract_type'],
        f_int_err: entry['f_int_err'],
        tau_time: entry['tau_time'],
        marker: {
            symbol: symbols[entry['extract_type']]
        }
    };

    var error_data = {
        x: entry['taustart_ts'],
        y: entry['f_int'],
        extract_type: entry['extract_type'],
        f_int: entry['f_int'],
        f_int_err: entry['f_int_err'],
        low: entry['f_int'] - entry['f_int_err'],
        high: entry['f_int'] + entry['f_int_err'],
        tau_time: entry['tau_time']
    };

    if (band in lightcurve_per_band) {
        lightcurve_per_band[band].push(data);
        error_per_band[band].push(error_data);
    } else {
        lightcurve_per_band[band] = [data];
        error_per_band[band] = [error_data];
    }

    // construc the plot bands. We want only unique plot bands
    from = entry['taustart_ts'],
    to = entry['taustart_ts'] + entry['tau_time'] * 1000
    if(!([from, to] in plot_bands_per_series)) {
        plot_bands_per_series[[from, to]] = true;
        plot_bands.push(
            {
                from: entry['taustart_ts'],
                to: entry['taustart_ts'] + entry['tau_time'] * 1000,
                color: 'rgba(68, 170, 213, .4)'
            }
        );
    }
});

// convert to highchart series
var series = [];
for(key in lightcurve_per_band) {
    data = lightcurve_per_band[key];
    error_data = error_per_band[key];

    series.push(
            {
                name: key,
                data: lightcurve_per_band[key],
                marker: {
                    symbol: 'square'
                }
            }
    );

    // to group datapoint and error bar together we need to add them sequensial
    series.push(
       {
           name: key + ' Error',
           type: 'errorbar',
           color: '#999',
           data: error_data
       }
    );
}

$(function () {
    $('#lightcurve').highcharts({
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },

        tooltip: {
          formatter: function () {
            return '<b></B>Time: </b>' + Highcharts.dateFormat('%Y %b %e %H:%M', this.point.x) +
                   '<br><b>flux (jY): </b>' + this.point.f_int +
                   '<br><b>extract_type: </b>' + this.point.extract_type +
                    '<br><b>Integrated Flux Error: </b>' + this.point.f_int_err +
                    '<br><b>Integration Time: </b>' + this.point.tau_time;
          }
        },

        title: {
            text: title
        },

        subtitle: {
            text: subtitle
        },

        xAxis: {
            type: 'datetime',
            labels: {
                formatter: function() {
                    return Highcharts.dateFormat('%b %e %H:%M', this.value);
                }
            },

            plotBands: plot_bands

        },

        yAxis: {
            title: {
                text: 'Flux (jY)'
            }
        },

        series: series,

        plotOptions: {
            areaspline: {
                fillOpacity: 0.5
            },
	        series: {
	            animation: false
	        },
        }
    });
});