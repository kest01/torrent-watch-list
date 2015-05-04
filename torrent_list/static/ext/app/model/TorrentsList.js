Ext.define('TorrentWatchList.model.TorrentsList', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'title', type: 'string'},
        {name: 'size', type: 'string'},
        {name: 'translation', type: 'string'},
        {name: 'url', type: 'string'},
        {name: 'seeders', type: 'string'},
        {name: 'leechers', type: 'string'},
        {name: 'torrentUrl', type: 'string'},
        {name: 'hubId', type: 'int'},
        {name: 'hub', type: 'string'}
    ]
});
