Ext.define('TorrentWatchList.model.Movie', {
    extend: 'Ext.data.Model',
    fields: [
        {name: 'id', type: 'int'},
        {name: 'nameFull', type: 'string'},
        {name: 'year', type: 'string'},
        {name: 'genre', type: 'string'},
        {name: 'description', type: 'string'},
        {name: 'actors', type: 'string'},
        {name: 'seeders', type: 'int'},
        {name: 'leechers', type: 'int'},
        {name: 'imdbId', type: 'string'},
        {name: 'kinopoiskId', type: 'string'},
        {name: 'rating', type: 'float'},
        {name: 'isNew', type: 'boolean'},
        {name: 'isReadyToDel', type: 'boolean', persist: false, convert: function(value, record) {
            var result = false;
//            console.log("isReadyToDel convert " + value);
            var genre = record.get('genre');
            if (genre && genre.toLowerCase().indexOf("ужас") > -1) {
                updateRecord(record, 'genre',
                    '<span style="color:red">' + genre + '</span>');
                result = true;
            }
            var translation = record.get('translation');
            if (translation) translation = translation.toLowerCase();
            if (translation && (translation.indexOf("любите") > -1 || translation.indexOf("одногол") > -1 || translation.indexOf("двухгол") > -1)) {
                updateRecord(record, 'translation',
                    '<span style="color:red">' + record.get('translation') + '</span>');
                result = true;
            }
            var imdbRating = record.get('imdbRating');
            if (imdbRating) {
                if (imdbRating > 0.1 && imdbRating < 5.0) {
                    result = true;
                }
            }
            return result;
        }},
        {name: 'skipped', type: 'boolean', persist: false, defaultValue: null, allowNull:true},
        {name: 'favorites', type: 'boolean'},
        {name: 'posterUrl', type: 'string'},
        {name: 'translation', type: 'string'}
    ],
    hasMany: [
        {
            model: 'TorrentWatchList.model.TorrentsList',
            name: 'torrents'
        }
    ]

});

function updateRecord(rec, fieldName, newValue) {
    rec.beginEdit();
    rec.set(fieldName, newValue);
    rec.dirty = false;
    rec.modified = {};
    rec.endEdit(true);
}