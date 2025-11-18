namespace ApiDePapas.Domain.Entities
{
    public enum ShippingStatus
    {
        created,
        reserved,
        in_transit,
        delivered,
        cancelled,
        in_distribution,
        arrived
    }
}