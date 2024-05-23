import _ from 'lodash';
/**
 * @class UpdateStrategyInterface
 * @classdesc STRATEGY PATTERN INTERFACE for controlling lights.
 *   There are some default settings all light types can use.  they include updateOffset and updateFrequency
 *   updateFrequency dictates how many heart beats should elapse before triggering a color update.
 *   There are MachineSetup.FREQUENCY heart beats per minute.
 *   updateOffset will allow a user to control which heart beat the color should update on,
 *   allowing for colors with the same frequency to update at different moments.
 * Example of options ->
 * {
 *     type: "???",  * Must be a string that matches one of the specific strategies, either Jump or Fade
 *      * Other options, depending on the strategy
 *     updateFrequency: 10
 *     updateOffset: 0
 * }
 */
class UpdateStrategyInterface {
    /**
     * constructor
     * @param {object} config
     */
    constructor(config) {
        this.type = _.get(config, 'type', 'Null');
        this.updateFrequency = _.get(config, 'updateFrequency', 10);
        this.updateOffset = _.get(config, 'updateOffset', 0);
    }
    /**
     * get default color from strategy
     * @return {Color} hsv
     */
    getDefaultColor() {
        return null;
    }

    /**
     * sets a default color depending on the strategy.
     * @param {Color} color
     */
    setDefaultColor(color) {
        // blank
    }

    /**
     * Returns the next color that should be shown.
     * @return {string} hex code
     */
    getNextColor() {
        return null;
    }
    /**
     * Return ths interval between setting new colors.
     * @return {Number}
     */
    getInterval() {
        return 99999;
    }

    /**
     * converts this class object to a plain object.
     * @return {object}
     */
    toPlainObject() {
        return {
            type: this.type,
            updateFrequency: this.updateFrequency,
            updateOffset: this.updateOffset,
        };
    }
}

export default UpdateStrategyInterface;
