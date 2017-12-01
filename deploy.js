const Deployer = require('ssh-deploy-release');
 
const options = {
    localPath: './',
    host: '77.47.207.42',
    username: 'mhama',
    passphrase: '',
    port: 2512,
    privateKeyFile: 'key.rsa',
    deployPath: '/var/www/vhost/path/to/project'
};
 
const deployer = new Deployer(options);
deployer.deployRelease(() => {
    console.log('Deployed !')
});