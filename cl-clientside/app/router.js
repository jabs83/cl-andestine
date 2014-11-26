import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.resource('organizations', { path: '/organizations' }, function() {
    this.route('organization', { path: '/organization/:id' });
  });
});

export default Router;
