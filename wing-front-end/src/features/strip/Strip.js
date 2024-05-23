import PropTypes from 'prop-types';
import { useEffect } from 'react';
import Spinner from 'react-bootstrap/Spinner';
import Stack from 'react-bootstrap/Stack';
import { useDispatch, useSelector } from 'react-redux';

import { getPositionFromLink } from '../../app/util';
import Light from '../light/Light';
import LightPane from '../light/LightPane';
import { fetchStripAction, getStrip } from './StripSlice';

/**
 * Strip
 * @param {object} param0
 * @return {ReactElement}
 */
function Strip({ self }) {
    const dispatch = useDispatch();
    const position = getPositionFromLink(self);
    const strip = useSelector((state) => getStrip(state, position));
    useEffect(() => {
        dispatch(fetchStripAction(position));
    }, []);

    if (!strip) {
        return <Spinner animation="border"
            variant="primary" />;
    }

    return <Stack gap={3}>
        <LightPane />
        {strip.lights.map((light) => <Light key={light.self}
            stripPosition={position}
            link={light.self} />)}
    </Stack>;
}

Strip.propTypes = {
    self: PropTypes.string.isRequired,
};

export default Strip;
