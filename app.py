import pandas as pd
import scipy.stats
import streamlit as st
import time

# Estas variables de estado se conservan cuando Streamlit vuelve a ejecutar el script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'caras', 'sellos', 'media']
    )

st.header('Lanzar una moneda')

st.write('Convencion del experimento: 1 = cara, 0 = sello')

# Grafica de la media acumulada
st.subheader('Media acumulada')
mean_chart = st.line_chart(
    pd.DataFrame({'media': [0.5]})
)

# Grafica de caras y sellos acumulados
st.subheader('Caras y sellos acumulados')
count_chart = st.line_chart(
    pd.DataFrame({
        'caras': [0],
        'sellos': [0]
    })
)


def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    cara_count = 0
    sello_count = 0

    for r in trial_outcomes:
        outcome_no += 1

        if r == 1:
            cara_count += 1
        else:
            sello_count += 1

        mean = cara_count / outcome_no

        # Actualiza la grafica de la media
        mean_chart.add_rows(
            pd.DataFrame({'media': [mean]})
        )

        # Actualiza la grafica de caras y sellos en la misma grafica
        count_chart.add_rows(
            pd.DataFrame({
                'caras': [cara_count],
                'sellos': [sello_count]
            })
        )

        time.sleep(0.05)

    return mean, cara_count, sello_count


number_of_trials = st.slider('Numero de intentos', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')

    st.session_state['experiment_no'] += 1

    mean, cara_count, sello_count = toss_coin(number_of_trials)

    st.subheader('Resultado del experimento')

    col1, col2, col3 = st.columns(3)

    col1.metric('Caras', cara_count)
    col2.metric('Sellos', sello_count)
    col3.metric('Media', round(mean, 4))

    new_result = pd.DataFrame(
        data=[
            [
                st.session_state['experiment_no'],
                number_of_trials,
                cara_count,
                sello_count,
                mean
            ]
        ],
        columns=['no', 'iteraciones', 'caras', 'sellos', 'media']
    )

    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            new_result
        ],
        axis=0
    )

    st.session_state['df_experiment_results'] = (
        st.session_state['df_experiment_results'].reset_index(drop=True)
    )

st.subheader('Historial de experimentos')
st.write(st.session_state['df_experiment_results'])