Ext.define('TorrentWatchList.store.MovieStore', {
    requires: [
        'TorrentWatchList.model.Movie'
    ],
    extend: 'Ext.data.Store',
    model: 'TorrentWatchList.model.Movie',

    proxy: {
        type: 'ajax',
        url: '/movies/',
        reader: {
            type: 'json'
            //rootProperty: 'users'
        },
        writer: {
            type: 'json',
            writeAllFields: false,
            allowSingle: false
        }
    },
    autoLoad: true
});