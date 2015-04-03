/**
 * Created by Konstantin on 03.04.2015.
 */
Ext.define('TorrentWatchList.view.main.TabView', {
    extend: 'Ext.tab.Panel',
    xtype: 'main-tabs',
    controller: 'tab-view',

    width: 400,
    height: 300,
    defaults: {
        bodyPadding: 10,
        autoScroll: true
    },
    items: [{
        title: 'Active Tab',
        html: 'lalala tab 1'
    }, {
        title: 'Inactive Tab',
        html: 'bebebe tab 2'
    }, {
        title: 'Disabled Tab',
        disabled: true
    }],

    listeners: {
        scope: 'controller',
        tabchange: 'onTabChange'
    }
});