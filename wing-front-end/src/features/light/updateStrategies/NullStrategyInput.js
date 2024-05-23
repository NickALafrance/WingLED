import PropTypes from 'prop-types';
import Accordion from 'react-bootstrap/Accordion';
import Form from 'react-bootstrap/Form';

import LightModel from '../../../app/models/light/Light';
import { LightModelPropTypes } from '../../../app/propTypes';
/**
 * draws inputs for null strategy.
 * @param {LightModel} light
 * @return {ReactElement}
 */
function NullStrategyInput({ light, updateLight }) {
    return <Accordion.Item eventKey="Null">
        <Accordion.Header onClick={() => {
            if (light.updateStrategy.type === 'Null') {
                return;
            }
            light.changeStrategies('Null');
            updateLight();
        }}>Static Strategy</Accordion.Header>
        <Accordion.Body>
            <Form.Label>Color Picker</Form.Label>
            <Form.Control style={{ width: '100%', height: '75px' }}
                type="color"
                defaultValue={light.color.hex}
                title="Choose a color for this LED"
                onChange={(event) => {
                    light.color.hex = event.target.value;
                    updateLight();
                } }
            />
        </Accordion.Body>
    </Accordion.Item>;
}

NullStrategyInput.propTypes = {
    light: LightModelPropTypes,
    updateLight: PropTypes.func.isRequired,
};

NullStrategyInput.defaultProps = {
    light: new LightModel(),
};

export default NullStrategyInput;
