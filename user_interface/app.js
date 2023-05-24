const max_value_graph = document.getElementById('max_value').getContext('2d');
const mean_value_graph = document.getElementById('mean_value').getContext('2d');
const btn_find_max = document.getElementById('find_max');

let max_value_chart = new Chart(max_value_graph, {});
let mean_value_chart = new Chart(mean_value_graph, {});

// function that will verify the parameters for the genetic algorithm
function verify_params(population, left_closure, right_closure, precision, prob_recombination, prob_mutation, num_of_steps){
    return population >= 1 && left_closure < right_closure && precision >= 1 && prob_recombination >= 1 
        && prob_recombination <= 100 && prob_mutation >=1 && prob_mutation <= 1 && num_of_steps >= 1;
}

btn_find_max.addEventListener("click", () => {
    const population = document.getElementsByName('population')[0].value;
    const left_closure = document.getElementsByName('left_closure')[0].value;
    const right_closure = document.getElementsByName('right_closure')[0].value;
    const a = document.getElementsByName('a')[0].value;
    const b = document.getElementsByName('b')[0].value;
    const c = document.getElementsByName('c')[0].value;
    const precision = document.getElementsByName('precision')[0].value;
    const prob_recombination = document.getElementsByName('prob_recombination')[0].value;
    const prob_mutation = document.getElementsByName('prob_mutation')[0].value;
    const num_of_steps = document.getElementsByName('num_of_steps')[0].value;

    // if the paramters are valid, continue with the request
    if(verify_params(population, left_closure, right_closure, precision, prob_recombination, prob_mutation, num_of_steps)){
        // configure the URL and the data for the GET request
        const url = "http://127.0.0.1:5000/start_genetic_algorithm";
        const data = new URLSearchParams({
            population: population,
            left_closure: left_closure, right_closure: right_closure,
            a: a, b: b, c: c, 
            precision: precision, 
            prob_recombination: prob_recombination, prob_mutation: prob_mutation,
            num_of_steps: num_of_steps
        });

        // in these arrays the information from the server
        // will be stored aka the evolution of mean and max for the algorithm's population
        let max_evolution_arr = [];
        let mean_evolution_arr = [];

        axios.get(`${url}?${data}`)
        .then((response) => {
            max_evolution_arr = response.data.max_evolution;
            mean_evolution_arr = response.data.mean_evolution;

            // before creating new charts, the old ones
            // must be destroyed
            max_value_chart.destroy();
            mean_value_chart.destroy();

            // create two separate chart.js charts
            max_value_chart = new Chart(max_value_graph, {
                type: 'line',
                data: {
                labels: Array.from({ length: max_evolution_arr.length }, (_, i) => `Steps ${i + 1}`),
                datasets: [{
                    label: 'Maximum evolution',
                    data: max_evolution_arr,
                    borderColor: 'rgb(75, 192, 192)',
                    fill: false
                }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                        beginAtZero: true
                        }
                    },
                    plugins: {
                        zoom: {
                          zoom: {
                            wheel: {
                              enabled: true
                            },
                            pinch: {
                              enabled: true
                            },
                            mode: 'xy'
                          }
                        }
                    }
                }
            });

            mean_value_chart = new Chart(mean_value_graph, {
                type: 'line',
                data: {
                labels: Array.from({ length: mean_evolution_arr.length }, (_, i) => `Steps ${i + 1}`),
                datasets: [{
                    label: 'Mean evolution',
                    data: mean_evolution_arr,
                    borderColor: 'rgb(75, 192, 192)',
                    fill: false
                }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                        beginAtZero: true
                        }
                    },
                    plugins: {
                        zoom: {
                          zoom: {
                            wheel: {
                              enabled: true
                            },
                            pinch: {
                              enabled: true
                            },
                            mode: 'xy'
                          }
                        }
                    }
                }
            });
        }).catch(err => console.log(err));
    } 
});

