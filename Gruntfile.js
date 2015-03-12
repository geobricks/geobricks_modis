'use strict';

module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        markdown: {
            readme: {
                files: {
                    'index.html': ['README.md']
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