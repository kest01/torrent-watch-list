/**
 * The main application class. An instance of this class is created by app.js when it calls
 * Ext.application(). This is the ideal place to handle application launch and initialization
 * details.
 */
Ext.define('TorrentWatchList.Application', {
    extend: 'Ext.app.Application',
    
    name: 'TorrentWatchList',

    stores: [
        'TorrentWatchList.store.MovieStore'
        // TODO: add global / shared stores here
    ],
    
    launch: function () {
        Ext.tip.QuickTipManager.init();
        // TODO - Launch the application
    }
});
