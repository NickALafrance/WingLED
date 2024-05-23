import axios from '../../app/axios';

/**
 * Fetch a specific light from the API.
 * @param {Number} stripPosition
 * @param {Number} position
 * @return {[Light]}
 */
export async function fetchLight({ stripPosition, position }) {
    const response = await axios.get(`strips/${stripPosition}/lights/${position}`);
    return response.data;
}

/**
 * update a specific light.
 * @param {Light} light
 * @return {string}
 */
export async function saveLight(light) {
    const response = await axios.put(
        `strips/${light.strip}/lights/${light.position}`,
        light,
    );
    return response.status;
}
