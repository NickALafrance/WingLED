import _ from 'lodash';
import PropTypes from 'prop-types';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import CloseButton from 'react-bootstrap/CloseButton';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

import LightModel from '../../../app/models/light/Light';
import { LightModelPropTypes } from '../../../app/propTypes';

/**
 * Jump strategy inputs.
 * @param {LightModel} light
 * @return {ReactElement}
 */
function JumpStrategyInput({ light, updateLight }) {
    return <Accordion.Item eventKey="Jump">
        <Accordion.Header onClick={() => {
            if (light.updateStrategy.type === 'Jump') {
                return;
            }
            light.changeStrategies('Jump');
            updateLight();
        }}>Jump Strategy</Accordion.Header>
        <Accordion.Body>
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>Jump Frequency</Form.Label>
                    <Form.Control type="number"
                        value={light.updateStrategy.updateFrequency}
                        onChange={(event) => {
                            light.updateStrategy.updateFrequency = parseInt(event.target.value);
                            updateLight();
                        }}
                        placeholder="10" />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Jump Offset from 0</Form.Label>
                    <Form.Control type="number"
                        value={light.updateStrategy.updateOffset}
                        onChange={(event) => {
                            light.updateStrategy.updateOffset = parseInt(event.target.value);
                            updateLight();
                        }}
                        placeholder="0" />
                </Form.Group>
                {_.map(light.updateStrategy.colors, ((color, i) => {
                    return <Container key={i}>
                        <Row>
                            <Col xs={9}>
                                <Form.Group key={i}
                                    className="mb-3">
                                    <Form.Label>
                            Color {i} (beat&nbsp;
                                        {i * light.updateStrategy.updateFrequency + light.updateStrategy.updateOffset}
                            )
                                    </Form.Label>
                                    <Form.Control style={{ width: '100%', height: '75px' }}
                                        type="color"
                                        value={color.hex}
                                        onChange={(event) => {
                                            color.hex = event.target.value;
                                            updateLight();
                                        }} />
                                </Form.Group>
                            </Col>
                            <Col xs={3}>
                                <CloseButton style={{ width: '100%', height: '75px', marginTop: '24px' }}
                                    className="float-end"
                                    onClick={() => {
                                        light.updateStrategy.removeColor(color);
                                        updateLight();
                                    }} />
                            </Col>
                        </Row>
                    </Container>;
                }))}
                <Button onClick={() => {
                    light.updateStrategy.addColor();
                    updateLight();
                }}>Add Jump</Button>
            </Form>
        </Accordion.Body>
    </Accordion.Item>;
}

JumpStrategyInput.propTypes = {
    light: LightModelPropTypes,
    updateLight: PropTypes.func.isRequired,
};

JumpStrategyInput.defaultProps = {
    light: new LightModel(),
};

export default JumpStrategyInput;
