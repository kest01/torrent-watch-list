/**
 * Created by Konstantin on 03.04.2015.
 */
Ext.define('TorrentWatchList.view.tabs.TabController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.tab-view',

    onTabChange: function(tabs, newTab, oldTab) {
        Ext.suspendLayouts();
        console.log('change tab to ' + newTab.title);
        var grid = newTab.items.getAt(0);
        var store = grid.store

        store.load({ params: { hubid: grid.hub_id} });
        store.on("load", function() {

            var button = Ext.ComponentQuery.query('#remove-button')[0];
            for (var i = 0; i < store.data.items.length; i++) {
                var row = store.data.items[i].data;
                console.log();
                if (row['isReadyToDel']) {
                    button.setDisabled(false);
                    return;
                }
            }
            button.setDisabled(true);
        });
        grid.getView().refresh();

        Ext.resumeLayouts(true);
    }

});