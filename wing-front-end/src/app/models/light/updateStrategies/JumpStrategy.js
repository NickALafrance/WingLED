import _ from 'lodash';

import Color from '../Color';
import UpdateStrategyInterface from './UpdateStrategyInterface';

/**
 * @class JumpStrategy
 * @classdesc  This strategy will JUMP the color of a light with the next color every update cycle.
 * It uses ONE option, which is COLORS.
 * COLORS should be an array of tuples, where each tuple is 1 integer between
 *  0 and 360 for Hue, and 2 floats between 0 and 1 for Saturation and Value.
 * Example of options ->
 * {
 *     type: "Jump",
 *     colors: [
 *         [0, 1, 1],    # RED
 *         [120, 1, 1],  # GREEN
 *         [240, 1, 1]   # BLUE
 *     ]
 * }
 */
class JumpStrategy extends UpdateStrategyInterface {
    /**
     * config
     * @param {object} config
     */
    constructor(config) {
        super(config);
        this.colors = _.get(config, 'colors', [[0, 1, 1]]).map((c) => new Color(c));
    }

    /**
     * Remove a color from list.
     * @param {Color} color
     */
    removeColor(color) {
        this.colors = _.without(this.colors, color);
    }

    /**
     * Add Color to list
     * @param {Color} color
     */
    addColor(color = new Color()) {
        this.colors.push(color);
    }

    /**
     * set default color.  The default color is the first color.
     * @param {Color} color
     */
    setDefaultColor(color) {
        this.colors = [color];
    }

    /**
     * get default color as object.
     * @return {object}
     */
    getDefaultColor() {
        return this.colors[0];
    }

    /**
     * get next color.
     * @return {string} hex
     */
    getNextColor() {
        if (_.isNil(this.currentColor)) {
            this.currentColor = 0;
        }
        this.currentColor++;
        try {
            return this.colors[this.currentColor % this.colors.length].hex;
        } catch (e) {
            return null;
        }
    }

    /**
     * interval is just the update frequency
     * @return {Number}
     */
    getInterval() {
        return this.updateFrequency;
    }

    /**
     * to plain object
     * @return {object}
     */
    toPlainObject() {
        const obj = super.toPlainObject();
        obj.colors = this.colors.map((c) => c.toArray());
        return obj;
    }
}

export default JumpStrategy;
