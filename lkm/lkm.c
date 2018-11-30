#include <linux/inet.h>
#include <linux/init.h>
#include <linux/ip.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/skbuff.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("COP5614 Final Project LKM");
MODULE_AUTHOR("Franklin Abodo/fabod001@fiu.edu");

static char *en0_ip_str = "127.0.0.1";

module_param(en0_ip_str, charp, S_IRUGO);

// static struct addr_in en0_addr_in = kmalloc(sizeof(struct in_addr), GFP_KERNEL);
// static uint8_t *en0_addr_in;
static __be32 en0_ip_hex;

struct nf_hook_ops nfho_in;
struct nf_hook_ops nfho_out;

/* This function is called when a packet is received. */
unsigned int hook_func_in(void *priv,
                          struct sk_buff *skb,
                          const struct nf_hook_state *state)
{
	struct iphdr *ip_header = (struct iphdr *)skb_network_header(skb);

  if (ip_header->daddr == en0_ip_hex)
  {
    trace_printk("|i|%u|%u|\n", en0_ip_hex, ip_header->daddr);
    trace_printk("|i|%pI4|%pI4|\n", &ip_header->saddr, &ip_header->daddr);
  }
  // else
  // {
  //   trace_printk("|_|%pI4|%pI4|", &ip_header->saddr, &ip_header->daddr);
  // }
	return NF_ACCEPT;
}

/* This function is called when a packet is sent. */
unsigned int hook_func_out(void *priv,
                           struct sk_buff *skb,
                           const struct nf_hook_state *state)
{
	struct iphdr *ip_header = (struct iphdr *)skb_network_header(skb);

  if (ip_header->saddr == en0_ip_hex)
  {
    trace_printk("|o|%u|%u|\n", en0_ip_hex, ip_header->saddr);
  	trace_printk("|o|%pI4|%pI4|\n", &ip_header->saddr, &ip_header->daddr);
  }
  // else
  // {
  //   trace_printk("|_|%pI4|%pI4|", &ip_header->saddr, &ip_header->daddr);
  // }
	return NF_ACCEPT;
}

int simple_init(void)
{
	printk(KERN_INFO "Initializing COP5614 Final Project LKM");
  printk("|%s|", en0_ip_str);
  en0_ip_hex = in_aton(en0_ip_str); //convert octet string to hex integer
  printk("|%u|", en0_ip_hex);

  nfho_in.hook = hook_func_in;
	nfho_in.hooknum = NF_INET_LOCAL_IN;
	nfho_in.pf = PF_INET;
	nfho_in.priority = NF_IP_PRI_LAST; //collecting the IP is a low priority

	nf_register_net_hook(&init_net, &nfho_in);

	nfho_out.hook = hook_func_out;
	nfho_out.hooknum = NF_INET_LOCAL_OUT;
	nfho_out.pf = PF_INET;
	nfho_out.priority = NF_IP_PRI_LAST; //collecting the IP is a low priority

	nf_register_net_hook(&init_net, &nfho_out);

	return 0;
}

void simple_exit(void)
{
	printk(KERN_INFO "Removing COP5614 Final Project LKM");

	nf_unregister_net_hook(&init_net, &nfho_in);
	nf_unregister_net_hook(&init_net, &nfho_out);
}

/* Macros for registering module entry and exit points. */
module_init(simple_init);
module_exit(simple_exit);
