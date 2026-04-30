#include <crypto/internal/aead.h>
#include <crypto/scatterwalk.h>
#include <crypto/if_alg.h>
#include <crypto/skcipher.h>
#include <crypto/null.h>
#include <linux/init.h>
#include <linux/list.h>
#include <linux/kernel.h>
#include <linux/mm.h>
#include <linux/module.h>
#include <linux/net.h>
#include <net/sock.h>

MODULE_DESCRIPTION("Remove aead");
MODULE_AUTHOR("Josko Plazonic");
MODULE_LICENSE("GPL");


static const struct af_alg_type myalgif_type_aead = {
        .bind           =       NULL,
        .release        =       NULL,
        .setkey         =       NULL,
        .setauthsize    =       NULL,
        .accept         =       NULL,
        .accept_nokey   =       NULL,
        .ops            =       NULL,
        .ops_nokey      =       NULL,
        .name           =       "aead",
        .owner          =       THIS_MODULE
};

/**
 * Module exits. 
 */
static int __init init_function(void) {   
	printk(KERN_INFO "Inside kernel space\n");
	af_alg_unregister_type(&myalgif_type_aead);
	return 0;
}

static void __exit exit_function(void) {   
}

module_init(init_function);
module_exit(exit_function);

