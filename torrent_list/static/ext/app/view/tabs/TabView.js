/**
 * Created by Konstantin on 03.04.2015.
 */
Ext.define('TorrentWatchList.view.tabs.TabView', {
    extend: 'Ext.tab.Panel',
    xtype: 'main-tabs',
    controller: 'tab-view',
    requires: [
        'TorrentWatchList.view.tabs.GridView',
        'TorrentWatchList.view.test.TestGrid'
    ],
    id: 'tab-view',
/*
    width: 400,
    height: 300,
*/
    defaults: {
        bodyPadding: 5,
//        scrollable: true
        layout: 'fit'
    },

    layout: {
        type: 'fit'
    },

    listeners: {
        scope: 'controller',
        tabchange: 'onTabChange'
    },
    tabBar: {
        items: [{
            xtype: 'tbfill'
        }, {
            xtype: 'button',
            id: 'remove-button',
            disabled: true,
//            padding: '5 5 5 5',
            text: 'Удалить отмеченное',
            handler: function() {
                //alert('You clicked the button!');
                var grid = this.up('#tab-view').getActiveTab().items.getAt(0);
                var store = grid.getStore();
                var  itemsToRemove = [];
                var addItem = function (record) {
                    var id = record.get('id');
                    var hubIds = []
                    if (grid.hub_id == 0) {
                        record.torrents().data.each(function(item) {
                            var hub = item.data['hubId'];
                            if (hubIds.indexOf(hub) == -1)
                                hubIds.push(hub)
                        });
                    } else {
                        hubIds.push(grid.hub_id)
                    }
                    return {
                        id: id,
                        hubIds: hubIds
                    }
                };
                store.each(function(record){
                    if (record.get('toRemove') != null) {
                        if (record.get('toRemove')) {
                            itemsToRemove.push(addItem(record));
                        }
                    } else if (record.get('isReadyToDel')) {
                        itemsToRemove.push(addItem(record));
                    }
                });
                if (itemsToRemove.length > 0) {
                    Ext.Ajax.request({
                        url: '/remove/',
                        method: 'POST',
                        //params: {arr: idsToRemove},
                        jsonData: itemsToRemove,
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
                console.log(itemsToRemove);

            }
        }]
    },

    initComponent: function() {
        this.callParent(arguments);
        var tabs = this;

        console.log('TabView.initComponent()');

        var tabMask = new Ext.LoadMask({
            msg: 'Please wait...',
            target: this.up()
        });
        tabMask.show();

        Ext.Ajax.request({
            url: '/hubs/',
            timeout: 20000,
            success: function(response){
                console.log("Successfully load data");
                var hubs = JSON.parse(response.responseText);
                var add_hub = function(hub) {
                    var s = '';
                    if (hub.new) s = ' <b> +' + hub.new + '</b>';
                    tabs.add({
                        title: hub.description + s,
                        items: [{
                            xtype: 'torrent-table-view',
                            hub_id: hub.id
                        }]
                    });
                };
                if (Array.isArray(hubs)) {
                    if (hubs.length > 1) {
                        tabs.add({
                            title: 'Все хабы',
                            items: [ {
                                xtype: 'torrent-table-view',
                                //xtype: 'test-grid',
                                hub_id: 0
                            }]
                        });
                    }
                    hubs.forEach(add_hub);
                } else {
                    add_hub(hubs);
                }
                tabs.setActiveTab(tabs.items.getAt(0));
                tabMask.hide();
            },
            failure: function(conn, response, options, eOpts) {
                tabMask.hide();
                showError(conn.responseText);
            }
        });
    }
});