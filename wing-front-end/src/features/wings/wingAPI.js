import axios from '../../app/axios';

/**
 * @return {*}
 */
export async function fetchWing() {
    const response = await axios.get('/strips');
    return response.data;
}
