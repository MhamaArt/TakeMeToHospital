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
    deployPath: '/home/mhama/project',
    onAfterDeploy(context, done) {
    	context.logger.log('Move dir to project/build/1.0');

		context.remote.exec('rm -rf /home/mhama/project/releases/build/1.0', () => {
	    	context.remote.exec(`cp -R /home/mhama/project/releases/${context.release.tag} /home/mhama/project/build/1.0/`, () => {
	    		context.remote.exec('rm -rf /home/mhama/project/releases/', done);
	    	});
	    });
    }
}).deployRelease();