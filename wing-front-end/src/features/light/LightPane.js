import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/esm/Button';
import Offcanvas from 'react-bootstrap/Offcanvas';
import { useDispatch, useSelector } from 'react-redux';

import LightModel from '../../app/models/light/Light';
import { closePane, getPane, isIdle, saveLightAction, setPane } from './LightSlice';
import FadeStrategyInput from './updateStrategies/FadeStrategyInput';
import JumpStrategyInput from './updateStrategies/JumpStrategyInput';
import NullStrategyInput from './updateStrategies/NullStrategyInput';

/**
 * Light Pane.
 * @return {ReactElement}
 */
function LightPane() {
    const dispatch = useDispatch();
    const light = new LightModel(useSelector(getPane));
    const ready = useSelector(isIdle);

    const saveLight = () => dispatch(saveLightAction(light.toPlainObject()));
    const updateLight = () => dispatch(setPane(light.toPlainObject()));

    return <Offcanvas show={light.loaded}
        onHide={() => dispatch(closePane())}>
        <Offcanvas.Header closeButton>
            Editing Strip # {light.strip} Light # {light.position}
        </Offcanvas.Header>
        <Offcanvas.Body>
            <Accordion activeKey={light.updateStrategy.type}
                className="text-center">
                <NullStrategyInput light={light}
                    updateLight={updateLight} />
                <JumpStrategyInput light={light}
                    updateLight={updateLight} />
                <FadeStrategyInput light={light}
                    updateLight={updateLight} />
            </Accordion>
            <div className="d-grid gap-2 my-4">
                <Button variant="primary"
                    disabled={!ready}
                    onClick={saveLight}
                    size="lg">Apply new settings</Button>
            </div>
            <Card body>
                <pre>{JSON.stringify(light.toPlainObject(), null, 2)}</pre>
            </Card>
        </Offcanvas.Body>
    </Offcanvas>;
}

export default LightPane;
