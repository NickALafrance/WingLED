import _ from 'lodash';
import { useEffect, useState } from 'react';

import Color from './Color';
import strategyFactory from './updateStrategies/StrategyFactory';

/**
 * @class Light
 * @classdesc Handles the data model for the light for consistency
 */
class Light {
    /**
     * given a light response form the pi, build a light model.
     * @param {object} light
     */
    constructor(light) {
        this.loaded = !_.isEmpty(light);
        this.strip = _.get(light, 'strip', 0);
        this.position = _.get(light, 'position', 0);
        this.color = new Color(
            _.get(light, 'hue', 0),
            _.get(light, 'saturation', 1),
            _.get(light, 'value', 1),
        );
        this.updateStrategy = strategyFactory(_.get(light, 'updateStrategy'));
    }

    /**
     * get URL for light.
     * @return {string}
     */
    getUrl() {
        return `strips/${this.strip}/lights/${this.position}`;
    }

    /**
     * Changes strategies.
     * @param {string} type
     */
    changeStrategies(type) {
        this.updateStrategy = strategyFactory({ type: type });
        this.updateStrategy.setDefaultColor(this.color);
    }

    /**
     * rotates color.
     * @return {string} color as hex
     */
    useCurrentColor() {
        const [color, setColor] = useState(this.color.hex);
        useEffect(() => {
            const interval = setInterval(
                () => setColor(this.updateStrategy.getNextColor()),
                this.updateStrategy.getInterval() * 250,
            );
            return () => clearInterval(interval);
        }, [this.updateStrategy.type]);
        return color;
    }

    /**
     * get the plain object representation of this class.
     * @return {object}
     */
    toPlainObject() {
        return {
            strip: this.strip,
            position: this.position,
            ...this.color.toObject(),
            updateStrategy: this.updateStrategy.toPlainObject(),
        };
    }
}

export default Light;
