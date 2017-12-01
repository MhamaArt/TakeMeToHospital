const Deployer = require('ssh-deploy-release');
const decompress = require('decompress');
const decompressTargz = require('decompress-targz');
const path = require('path');
 
const options = {
    localPath: './',
    host: '77.47.207.42',
    username: 'mhama',
    password: 'Rossignol',
    //passphrase: '',
    port: 2512,
    // privateKeyFile: './key.rsa',
    deployPath: '/home/mhama/project'
};
 
const deployer = new Deployer(options);
deployer.deployRelease((context) => {
	const archivePath = context.release.path;

	decompress(path.join(archivePath, 'release.tar.gz'), 'dist', {
	    plugins: [
	        decompressTargz()
	    ]
	}).then(() => {
	    console.log('Files decompressed');
	});

    console.log('Deployed !')
});