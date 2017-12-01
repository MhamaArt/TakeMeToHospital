const Deployer = require('ssh-deploy-release');
const path = require('path');

new Deployer({
    localPath: './',
    host: '77.47.207.42',
    username: 'mhama',
    password: 'Rossignol',
    //passphrase: '',
    port: 2512,
    // privateKeyFile: './key.rsa',
    deployPath: '/home/mhama/project/releases',
    onAfterDeploy(context, done) {
    	context.logger.log('Move dir to project/build/');
        /*
		context.remote.exec('rm -rf /home/mhama/project/build/active', () => {
	    	context.remote.exec(`cp -R /home/mhama/project/releases/${context.release.tag} /home/mhama/project/build/active`, () => {
	    		context.remote.exec('rm -rf /home/mhama/project/releases/', done);
	    	});
	    });*/
    }
}).deployRelease();