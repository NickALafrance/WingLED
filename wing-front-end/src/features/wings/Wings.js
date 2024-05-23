import './wings.css';

import { useEffect } from 'react';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import ProgressBar from 'react-bootstrap/ProgressBar';
import Row from 'react-bootstrap/Row';
import { useDispatch, useSelector } from 'react-redux';

import Strip from '../strip/Strip';
import { fetchWingAction, getWing } from './wingSlice';

/**
 * wings
 * @return {JSX.Element}
 */
function Wings() {
    const dispatch = useDispatch();
    const wings = useSelector(getWing);

    useEffect(() => {
        dispatch(fetchWingAction());
    }, []);

    if (!wings) {
        return <ProgressBar animated
            now={100}
            variant="primary" />;
    }

    return <Container p={4}
        className="wings">
        <Row>
            {wings.strips.map((strip) => <Col key={strip.self}><Strip {...strip} /></Col>)}
        </Row>
    </Container>;
}

export default Wings;
