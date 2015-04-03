/**
 * This class is the main view for the application. It is specified in app.js as the
 * "autoCreateViewport" property. That setting automatically applies the "viewport"
 * plugin to promote that instance of this class to the body element.
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('TorrentWatchList.view.main.Main', {
    extend: 'Ext.container.Container',
    requires: [
        'TorrentWatchList.store.MovieStore',
        'TorrentWatchList.view.main.MainController',
        'TorrentWatchList.view.main.MainModel',
        'TorrentWatchList.view.tabs.TabView',
        'TorrentWatchList.view.tabs.TabController'
    ],

    xtype: 'app-main',
    
    controller: 'main',
    viewModel: {
        type: 'main'
    },

    layout: {
        type: 'fit'
    },

/*    items: [{
        xtype: "torrent-table-view",
        padding: "20 40 20 40"
    }]*/
    items: [{
        xtype: "main-tabs",
        padding: "20 20 20 20"
    }]
});
