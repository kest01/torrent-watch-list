/**
 * Created by Konstantin on 20.12.2014.
 */
/**
 * This example shows how to create Widgets in grid columns. Widgets are lightweight
 * components with a simpler lifecycle.
 */

//var tooltips = new Ext.util.HashMap();
var tooltip;
var movieStore;



Ext.define('TorrentWatchList.view.main.TableView', {
    extend: 'Ext.grid.Panel',
    requires: [
        'TorrentWatchList.store.MovieStore',
        'TorrentWatchList.model.TorrentsList',
        'Ext.grid.column.Action'
    ],
    xtype: 'torrent-table-view',
    store: 'TorrentWatchList.store.MovieStore',
    collapsible: false,
    height: 350,
    width: 1050,
    title: 'Torrents list',
//    bufferedRenderer: false,
    viewConfig: {
        stripeRows: true,
        enableTextSelection: true,
        markDirty: false
    },
    trackMouseOver: true,
    tools:[
        {
            type:'refresh',
            tooltip: 'Sync',
            cls:'torrents-sync-button',
            handler: function(event, toolEl, panel){
                var grid = panel.up();
                var store = grid.getStore();
                var idsToSkip = [];
                store.each(function(record){
                    if (record.get('skipped') != null) {
                        if (record.get('skipped')) {
                            idsToSkip.push(record.get('id'));
                        }
                    } else if (record.get('isReadyToDel')) {
                        idsToSkip.push(record.get('id'));
                    }
                });
                if (idsToSkip.length > 0) {
                    Ext.Ajax.request({
                        url: 'http://localhost:8080/torrents/skip',
                        method: 'POST',
                        //params: {arr: idsToSkip},
                        jsonData: idsToSkip,
                        success: function() {
                            store.load();
//                            grid.getView().refresh();
                            console.log('Grid reloaded after update');
                        },
                        failure: function(response) {
                            Ext.MessageBox.show({
                                title: response.status + ' ' + response.statusText,
                                msg: response.responseText,
                                buttons: Ext.MessageBox.OK,
                                icon: Ext.MessageBox.ERROR
                            });
                        }
                    });
                }
                console.log(idsToSkip);

            }
        }],
    initComponent: function () {
        var me = this;

        me.columns = [{
            xtype: 'actioncolumn',
            width: 34,
            sortable: false,
            menuDisabled: true,
            tdCls: "vertical-align-class",
            items: [{
                iconCls: "icon-size",
                tooltip: 'First showed movie',
                scope: this,
                getClass: function(v, metadata, r) {
                    if (r.get('isNew')) {
                        return 'is-new';
                    }
                }
            }]
        },{
            xtype: 'gridcolumn',
            dataIndex : 'posterUrl',
            text : 'Poster',
            sortable : false,
            align: 'center',
            width: 120,
//            width: 104,
            renderer: function(val, meta, record, rowIndex) {
                return '<img src="' + val +  '" width="100" onmouseover="showPoster(' + rowIndex + ')" onmouseout="hidePoster()" id="tooltip_img_' + meta.record.internalId + '"/>';
            }

        }, {
            text: 'Description',
                flex: 1,
//            width: auto,
            cellWrap: true,
            dataIndex: 'nameFull',
            sortable : false,
            renderer: function(val, meta, record) {
                return '<b>Название</b>: ' + val + '<br/>'
                    + "<b>Год выпуска</b>: " + record.raw.year + "<br/>"
                    + "<b>Жанр</b>: " + record.raw.genre + "<br/>"
                    + "<b>Перевод</b>: " + record.raw.translation + "<br/>"
                    + "<b>Описание</b>: " + record.raw.description + "<br/>"
                    + "<b>Актеры</b>: " + record.raw.actors;
            }
        }, {
            text: 'S',
            width: 50,
            tdCls: "vertical-align-class",
            align: 'center',
            dataIndex: 'seeders'
        }, {
            text: 'L',
            width: 50,
            tdCls: "vertical-align-class",
            align: 'center',
            dataIndex: 'leechers'
        }, {
            text: 'IMDB',
            width: 120,
            tdCls: "vertical-align-class",
            align: 'center',
            dataIndex: 'imdbRating',
            renderer: function(val, meta, record) {
                return '<a href="http://www.imdb.com/title/' + record.raw.imdbId + '/" target="_blank" rel="nofollow"><img src="http://imdb.snick.ru/ratefor/02/' + record.raw.imdbId +  '.png"/></a>';
            }
        }, {
            xtype: 'actioncolumn',
            width: 52,
            sortable: false,
            menuDisabled: true,
            tdCls: "vertical-align-class",
            align: 'center',
            items: [{
                tooltip: 'Download torrent',
                scope: this,
                getClass: function() {
                    return "download";
                },
                handler: function(grid, rowIndex, colIndex, item, event, record, row) {
                    console.log("Download torrent");
/*                    var torrentStore = Ext.create('Ext.data.ArrayStore', {
                        model: 'TorrentWatchList.model.TorrentsList',
                    });
                    var torrents = record.get("torrents");
                    if (torrents && Array.isArray(torrents)) {*/
                    var torrentStore = record._torrents;
                    var height = 80 + torrentStore.getCount() * 55;
                    var eventCount = 0;
                    var closeWin = function(e, t) {
                        if (eventCount++ == 0) return;
                        var el = win.getEl();

                        if (!(el.dom === t || el.contains(t))) {
                            Ext.getBody().un('click', closeWin);
                            win.close();
                        }
                    }


                    var win = Ext.create('Ext.window.Window', {
                        title: 'Hello',
                        height: height,
                        width: 1000,
                        modal: true,
                        layout: 'fit',
                        items: {
                            xtype: 'grid',
                            border: false,
                            columns: [
                                {
                                    text: 'Title',
                                    flex: 1,
                                    cellWrap: true,
                                    dataIndex: 'title',
                                    menuDisabled: true,
                                    sortable : true,
                                    renderer: function(val, meta, record) {
                                        return '<a href="' + record.get("url") + '" target="_blank">' + record.get("title") + '</a>';
                                    }
                                }, {
                                    text: 'Translation',
                                    flex: 1,
                                    cellWrap: true,
                                    dataIndex: 'translation',
                                    menuDisabled: true,
                                    sortable : true
                                }, {
                                    text: 'Size',
                                    width: 70,
                                    cellWrap: true,
                                    dataIndex: 'size',
                                    menuDisabled: true,
                                    tdCls: "vertical-align-class",
                                    sortable : true
                                }, {
                                    text: 'Seeders',
                                    width: 60,
                                    dataIndex: 'seeders',
                                    align: 'center',
                                    tdCls: "vertical-align-class",
                                    menuDisabled: true,
                                    sortable : true
                                }, {
                                    text: 'Leechers',
                                    width: 60,
                                    align: 'center',
                                    tdCls: "vertical-align-class",
                                    dataIndex: 'leechers',
                                    menuDisabled: true,
                                    sortable : true
                                }, {
                                    width: 40,
                                    menuDisabled: true,
                                    sortable : false,
                                    renderer: function(val, meta, record) {
                                        return '<a href="' + record.get("torrentUrl") + '" rel="nofollow"><img src="resources/1420933969_download.png"/></a>';
                                    }
                                }
                            ],
                            store: torrentStore
                        },
                        listeners: {
                            show: function() {
//                                Ext.getBody().on('click', closeWin);
                            }
                        }
                    });
                    win.show();


//                    }
                }
            }]
        }, {
            xtype: 'actioncolumn',
            width: 34,
            sortable: true,
            menuDisabled: true,
            tdCls: "vertical-align-class",
            items: [{
                tooltip: 'Mark for deletion',
                scope: this,
                handler: function(grid, rowIndex, colIndex, item, event, record) {
                    if (record.get('skipped') != null) {
                        if (record.get('skipped')) {
                            record.set('skipped', false);
                        } else{
                            record.set('skipped', true);
                        }
                    } else if (record.get('isReadyToDel')) {
                        record.set('skipped', false);
                    } else{
                        record.set('skipped', true);
                    }
                },
                getClass: function(v, metadata, r) {
                    if (r.get('skipped') != null) {
                        if (r.get('skipped')) {
                            return 'skipped-true';
                        } else{
                            return 'skipped-false';
                        }
                    } else if (r.get('isReadyToDel')) {
                        return 'skipped-true';
                    } else{
                        return 'skipped-false';
                    }
                }
            }]
        }, {
            xtype: 'actioncolumn',
            width: 34,
            sortable: true,
            menuDisabled: true,
            tdCls: "vertical-align-class",
            items: [{
                tooltip: 'Add to favorites',
                scope: this,
                handler: function(grid, rowIndex, colIndex, item, event, record) {
                    record.beginEdit();
                    if (record.get('favorites')) {
                        record.set('favorites', false);
                    } else {
                        record.set('favorites', true);
                    }
                    record.endEdit();
                    record.store.sync();
                },
                getClass: function(v, metadata, r) {
                    if (r.get('favorites')) {
                        return 'favorite';
                    } else{
                        return 'notfavorite';
                    }
                }
            }]
        }];

        me.callParent();
    },
    listeners: {
    }


});

function showPoster(rowIndex) {
//    console.log("Show poster for row " + rowIndex );
//    var tip = tooltips.get(rowIndex);
    if (!tooltip) {
        tooltip = Ext.create('Ext.tip.ToolTip', {
            target: "tooltip_img_1",
            html: '',
            getTargetXY: function() {
                return [500, 20];
            }
        });
    }
    if (!movieStore) {
        movieStore = Ext.data.StoreManager.lookup('TorrentWatchList.store.MovieStore');
        if (!movieStore)
            return;
    }
    var url = movieStore.getAt(rowIndex).get('posterUrl');
    if (!url) return;
    tooltip.update('<img src="' + url + '"/>');
    tooltip.show();
}

function hidePoster() {
//    console.log("Hide poster for row " + rowIndex );
    if (tooltip) {
        tooltip.hide();
    }
}