'use strict';

module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        markdown: {
            readme: {
                files: {
                    'index.html': ['README.md']
                }
            },
            options: {
                template: 'index.tmpl.html',
                autoTemplate: false,
                postCompile: function(src, context) {
                    return src.replace(/<pre>/g, '<pre class="prettyprint">');
                }
            }
        }
    });

    grunt.registerTask('default', [
        'markdown'
    ]);

    //grunt.loadNpmTasks('grunt-contrib-clean');
    //grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-markdown');
};