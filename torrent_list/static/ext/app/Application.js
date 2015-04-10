/**
 * The main application class. An instance of this class is created by app.js when it calls
 * Ext.application(). This is the ideal place to handle application launch and initialization
 * details.
 */
//var tabMask;

Ext.define('TorrentWatchList.Application', {
    extend: 'Ext.app.Application',
    
    name: 'TorrentWatchList',

    stores: [
        'TorrentWatchList.store.MovieStore',
        'TorrentWatchList.view.test.TestStore'

    ],
    
    launch: function () {
        Ext.tip.QuickTipManager.init();

    }
});

function showError(message) {
        console.error("Error message: ", message);
        Ext.MessageBox.show({
            title: 'Error!',
            msg: "Please see application log for detail.",
            cls: 'sm-alert-dialog',
            buttons: Ext.MessageBox.OK
        });
    };