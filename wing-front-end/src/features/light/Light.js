import PropTypes from 'prop-types';
import { useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import { useDispatch, useSelector } from 'react-redux';

import LightModel from '../../app/models/light/Light';
import { getPositionFromLink } from '../../app/util';
import { fetchLightAction, getLight, setPane } from './LightSlice';
/**
 * Light
 * @param {*} prop
 * @return {ReactElement}
 */
function Light({ link, stripPosition }) {
    const position = getPositionFromLink(link);
    const dispatch = useDispatch();
    const light = new LightModel(useSelector((state) => getLight(state, stripPosition, position)));
    useEffect(() => {
        dispatch(fetchLightAction({ stripPosition, position }));
    }, []);
    const color = light.useCurrentColor();

    if (!light.loaded) {
        return <Spinner animation="border"
            variant="primary" />;
    }

    return <div><Button size="lg"
        onClick={() => dispatch(setPane(light.toPlainObject()))}
        style={{ backgroundColor: color ?? light.color.hex }}>&nbsp;</Button></div>;
}

Light.propTypes = {
    link: PropTypes.string.isRequired,
    stripPosition: PropTypes.number.isRequired,
};

export default Light;
