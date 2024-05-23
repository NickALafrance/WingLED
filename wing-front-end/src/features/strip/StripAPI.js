import axios from '../../app/axios';

/**
 * Fetch a specific strip from the API.
 * @param {Number} position
 * @return {[Strip]}
 */
export async function fetchStrip(position) {
    const response = await axios.get(`strips/${position}`);
    return response.data;
}
